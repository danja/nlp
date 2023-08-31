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
"""

from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
import json
import csv

IP_ADDRESS = '127.0.0.1'
PORT = 9669
USER = 'root'
PASSWORD = 'password'
SPACE = 'guardians'


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


# Importing the required modules for demonstration


def extract_relationships(json_rel_str):
    """
    Extracts the significant parts of the relationships from the given JSON string,
    returned by a NebulaGraph query.

    Parameters:
        json_rel_str (str): The JSON string to extract information from.

    Returns:
        list: A list of dictionaries containing 'src', 'relationship', and 'dst' fields.
    """
    try:
        # Parse the JSON string into a dictionary
        json_data = json.loads(json_rel_str)

        # Initialize a list to store the extracted relationships
        extracted_relationships = []

        # Loop through the "data" to extract the required information
        for entry in json_data.get('results', [{}])[0].get('data', []):
            src = entry.get('row', [{}])[0].get('src.name', 'N/A')
            relationship = entry.get('row', [{}])[0].get(
                'relationship.relationship', 'N/A')
            dst = entry.get('row', [{}])[0].get('dst.name', 'N/A')

            # Append the extracted relationship to the list
            extracted_relationships.append(
                {"src": src, "relationship": relationship, "dst": dst})

        return extracted_relationships

    except json.JSONDecodeError as e:
        return f"Failed to parse string as JSON: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


# Entities
resp = client.execute_json('MATCH (v:entity) RETURN v')

json_str = resp.decode('utf-8')

entities = extract_entities(json_str)

text_to_file(str(entities), './entities.json')

# Relationships
resp_rel = client.execute_json(
    'MATCH (src:entity)-[e:relationship]->(dst:entity) RETURN src, e, dst LIMIT 3')
json_rel_str = resp_rel.decode('utf-8')

text_to_file(json_rel_str, 'relationships-raw.json')

relationships = extract_relationships(json_rel_str)
text_to_file(str(relationships), './relationships.json')

# Release resources
client.release()
