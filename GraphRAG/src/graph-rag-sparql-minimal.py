
#
# Preparation :
#
# * pip install sparqlwrapper
# * Make a SPARQL endpoint available, add URL below
# * Add OpenAI API key below
#

from llama_index import download_loader
from llama_index.query_engine import KnowledgeGraphQueryEngine
import os
import logging
import sys
from llama_index import (
    VectorStoreIndex,
    KnowledgeGraphIndex,
    ServiceContext,
    SimpleDirectoryReader,
)

from llama_index.storage.storage_context import StorageContext
from llama_index.graph_stores import SparqlGraphStore
from llama_index.llms import OpenAI
from IPython.display import Markdown, display
from llama_index import load_index_from_storage
import os
import sys
import openai


os.environ["OPENAI_API_KEY"] = ""

openai.api_key = ""

# logging.basicConfig(
#    stream=sys.stdout, level=logging.INFO
# )  # logging.DEBUG for more verbose output

logging.basicConfig(filename='loggy.log', filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('graph-rag-sparql-minimal HERE')

####
# SPARQL Config
ENDPOINT = 'https://fuseki.hyperdata.it/llama_index_sparql-test/'
GRAPH = 'http://purl.org/stuff/guardians'
BASE_URI = 'http://purl.org/stuff/data'

graph_store = SparqlGraphStore(
    sparql_endpoint=ENDPOINT,
    sparql_graph=GRAPH,
    sparql_base_uri=BASE_URI,
)
storage_context = StorageContext.from_defaults(graph_store=graph_store)

llm = OpenAI(temperature=0, model="text-davinci-002")
service_context = ServiceContext.from_defaults(llm=llm, chunk_size=512)


WikipediaReader = download_loader("WikipediaReader")

loader = WikipediaReader()

documents = loader.load_data(
    pages=['Guardians of the Galaxy Vol. 3'], auto_suggest=False)

kg_index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    service_context=service_context,
    max_triplets_per_chunk=10,
    # space_name=space_name,
    # edge_types=edge_types,
    # rel_prop_names=rel_prop_names,
    # tags=tags,
    sparql_endpoint=ENDPOINT,
    sparql_graph=GRAPH,
    sparql_base_uri=BASE_URI,
    include_embeddings=True,
)

# ----
# from 4. Persist and Load from disk Llama Indexes(Optional)

# vector_index.storage_context.persist(persist_dir='./storage_vector')
logger.info('#### 4')

# storage_context = StorageContext.from_defaults(
#    persist_dir='./storage_graph', graph_store=graph_store)
# kg_index = load_index_from_storage(
#    storage_context=storage_context,
#    service_context=service_context,
#    include_embeddings=True,
#    sparql_endpoint=ENDPOINT,
#    sparql_graph=GRAPH,
#    sparql_base_uri=BASE_URI,
# )

# exit(0)

# FileNotFoundError: [Errno 2] No such file or directory: '/home/danny/AI/nlp/GraphRAG/src/storage_graph/docstore.json'
# copied files I found in a storage_vector/docstore.json into /home/danny/AI/nlp/GraphRAG/src/storage_graph/

storage_context_vector = StorageContext.from_defaults(
    persist_dir='./storage_vector')
vector_index = load_index_from_storage(
    service_context=service_context,
    storage_context=storage_context_vector
)

# FileNotFoundError: [Errno 2] No such file or directory: '/home/danny/AI/nlp/GraphRAG/src/storage_vector/docstore.json'
# copied storage_graph/* to vector_graph

# ----
# from 5.2 Graph RAG query engine
logger.info('#### 5.2')
kg_rag_query_engine = kg_index.as_query_engine(
    include_text=False,
    retriever_mode="keyword",
    response_mode="tree_summarize",
)

# 6.2 Graph RAG
logger.info('#### 6.2')
response_graph_rag = kg_rag_query_engine.query("Tell me about Peter Quill.")
print({response_graph_rag})
display(Markdown(f"<b>{response_graph_rag}</b>"))
