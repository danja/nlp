""""
Queries NebulaGraph store, dumps data in RDF/Turtle format

For now, special case (and hacky), just works against this setup :

CREATE SPACE guardians(vid_type=FIXED_STRING(256), partition_num=1, replica_factor=1);
:sleep 10;
USE guardians;
CREATE TAG entity(name string);
CREATE EDGE relationship(relationship string);
:sleep 10;
CREATE TAG INDEX entity_index ON entity(name(256));

pip install sparqlwrapper
"""
import re
import json
import csv
import random
import string

from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config


# NebulaGraph Config
IP_ADDRESS = '127.0.0.1'
PORT = 9669
USER = 'root'
PASSWORD = 'password'
SPACE = 'guardians'

# SPARQL Config
ENDPOINT = 'https://fuseki.hyperdata.it/llama_index-test/'
GRAPH = 'http://purl.org/stuff/guardians'
BASE_URL = "http://purl.org/stuff"


# Initialize connection pool
config = Config()
config.max_connection_pool_size = 10

# Replace the IP and port with your NebulaGraph database IP and port
connection_pool = ConnectionPool()
ok = connection_pool.init([(IP_ADDRESS, PORT)], config)

# Connect to the database
client = connection_pool.get_session(USER, PASSWORD)

# Switch to the 'guardians' space
client.execute('USE '+SPACE)

# Function to write data to CSV


def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def text_to_file(text, filename):
    text_file = open(filename, 'w')
    text_file.write(text)
    text_file.close()

# NEEDS SPECIAL CHAR ENCODING AND/OR SANITIZATION FOR RDF LITERALS


def extract_entities(json_data):
    """
    Extracts the value of "spaceName" and a series of dictionaries from the given JSON data,
    with added error handling and string parsing.

    Parameters:
        json_data (dict/str): The JSON data to extract information from, either as a dictionary or a string.

    Returns:
        tuple: The value of "spaceName" and a list of dictionaries with "id" and "value",
               or an error message.
    """
    # Attempt to parse string into a dictionary if the input is a string
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError as e:
            return f"Failed to parse string as JSON: {e}", None

    if not isinstance(json_data, dict):
        return "Input is not a dictionary", None

    try:
        # Extract the value of "spaceName"
        space_name = json_data.get('results', [{}])[0].get('spaceName', 'N/A')

        # Initialize a list to store the series of dictionaries
        extracted_data = []

        # Loop through the "data" to extract the required information
        for entry in json_data.get('results', [{}])[0].get('data', []):
            meta_id = entry.get('meta', [{}])[0].get('id', 'N/A')
            entity_name = entry.get('row', [{}])[0].get('entity.name', 'N/A')
            extracted_data.append({"id": meta_id, "value": entity_name})

        return space_name, extracted_data
    except Exception as e:
        return f"An error occurred: {e}", None

# Modifying the extract_relationships function again to correctly capture the 'dst' field


# Finalizing the extract_relationships function to produce output in the format [{"s": ..., "p": ..., "o": ...}]
def extract_relationships(json_rel_str):
    """
    Extracts the significant parts of the relationships from the given JSON string,
    returned by a NebulaGraph query.

    Parameters:
        json_rel_str (str): The JSON string to extract information from.

    Returns:
        list: A list of dictionaries containing 's', 'p', and 'o' fields.
    """
    try:
        # Parse the JSON string into a dictionary
        json_data = json.loads(json_rel_str)

        # Initialize a list to store the extracted relationships
        extracted_relationships = []

        # Loop through the "data" to extract the required information
        for entry in json_data.get('results', [{}])[0].get('data', []):
            row_list = entry.get('row', [{}])

            # Extracting source vertex, relationship, and destination vertex
            s = next((row.get('entity.name', 'N/A')
                     for row in row_list if 'entity.name' in row), 'N/A')
            p = next((row.get('relationship', 'N/A')
                     for row in row_list if 'relationship' in row), 'N/A')
            o = next((row.get('entity.name', 'N/A')
                     for row in row_list if 'entity.name' in row and row.get('entity.name') != s), 'N/A')

            # Append the extracted relationship to the list
            extracted_relationships.append({"s": s, "p": p, "o": o})
        return extracted_relationships

    except json.JSONDecodeError as e:
        return f"Failed to parse string as JSON: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


def remove_duplicates(json_structure):
    # Use a set to keep track of unique dictionaries
    unique_set = set()

    # List to store unique dictionaries
    unique_list = []

    for entry in json_structure:
        # Convert dictionary to a tuple of its items (key-value pairs) for hashing
        tuple_entry = tuple(sorted(entry.items()))

        # Check if tuple is unique
        if tuple_entry not in unique_set:
            # Add tuple to the set
            unique_set.add(tuple_entry)

            # Add the original dictionary to the list
            unique_list.append(entry)

    return unique_list


def escape_for_rdf(input_str):
    # Escape control characters
    input_str = input_str.encode("unicode_escape").decode("utf-8")

    # Escape single and double quotes
    input_str = re.sub(r'(["\'])', r'\\\1', input_str)

    return input_str


def make_id():
    """
    Generate a random 4-character string using only numeric characters and capital letters.
    """
    characters = string.ascii_uppercase + string.digits  # All available characters
    return ''.join(random.choice(characters) for _ in range(4))

# Re-defining the function and testing it again


def confirm_fragment(name_value_list, new_pair):
    """
    Add a new name-value pair to the list only if the value doesn't already exist.
    Return the name part corresponding to the value of the added or existing pair.

    Parameters:
    - name_value_list: List of dictionaries containing name-value pairs
    - new_pair: Dictionary containing a single new name-value pair

    Returns:
    - Name part corresponding to the value
    """
    # print(new_pair)
    new_value = list(new_pair.values())[0]  # Extract the value from new_pair

    # Check if the value exists in the list
    for d in name_value_list:
        if new_value in d.values():
            return list(d.keys())[0]

    # Add the new pair if the value is unique
    name_value_list.append(new_pair)
    return list(new_pair.keys())[0]

# Test the function with a unique value
# existing_list = [{'name1': 'value1'}, {'name2': 'value2'}]
# new_pair = {'name3': 'value3'}
# result_unique = add_or_get_name(existing_list, new_pair)

# Test the function with a non-unique value
# new_pair_non_unique = {'name4': 'value1'}
# result_non_unique = add_or_get_name(existing_list, new_pair_non_unique)
# result_unique, result_non_unique


# makes triples from simple json (without prefixes)
def to_rdf(json_data):
    rdf_data = ''
    url_string_pairs = []

    for entry in json_data:
        triplet_fragment = '#T'+make_id()  # should be unique

        s_string = entry['s']
        p_string = entry['p']
        o_string = entry['o']

        # make a new fragment, but the string might have been seen before, if it has been, replace with existing fragment
        s_fragment = '#E'+make_id()
        s_fragment = confirm_fragment(url_string_pairs, {s_fragment: s_string})
        p_fragment = '#R'+make_id()
        p_fragment = confirm_fragment(url_string_pairs, {p_fragment: p_string})
        o_fragment = '#E'+make_id()
        o_fragment = confirm_fragment(url_string_pairs, {o_fragment: o_string})

        # print(f"subject {s}, predicate {p}, object {o}")
        triple = f"""
                        <{triplet_fragment}> a er:Triplet ;
                                er:subject <{s_fragment}> ;
                                er:property <{p_fragment}> ;
                                er:object <{o_fragment}> .

                        <{s_fragment}> a er:Entity ;
                                er:value "{s_string}" .

                        <{p_fragment}> a er:Relationship ;
                                er:value "{p_string}" .

                        <{o_fragment}> a er:Entity ;
                                er:value "{o_string}" .
                """
        rdf_data = rdf_data + triple
    return rdf_data

# test_str = 'This is "a" \n test string.'
# escaped_str = escape_for_rdf(test_str)
# print(escaped_str)


# Entities
resp = client.execute_json('MATCH (v:entity) RETURN v')

json_str = resp.decode('utf-8')

entities = extract_entities(json_str)

text_to_file(str(entities), './entities.json')

# Relationships
resp_rel = client.execute_json(
    'MATCH (src:entity)-[e:relationship]->(dst:entity) RETURN src, e, dst')  # LIMIT 10

json_rel_str = resp_rel.decode('utf-8')

# text_to_file(json_rel_str, 'relationships-raw.json')

relationships = extract_relationships(json_rel_str)
relationships = remove_duplicates(relationships)
text_to_file(str(relationships), './relationships.json')

rdf = to_rdf(relationships)

text_to_file(rdf, './guardians.ttl')

# Release resources
client.release()
