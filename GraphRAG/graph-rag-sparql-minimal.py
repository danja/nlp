from IPython.display import Markdown, display
from llama_index.llms import OpenAI
from llama_index.graph_stores import SparqlStore
from llama_index.storage.storage_context import StorageContext
from llama_index import (
    KnowledgeGraphIndex,
    ServiceContext,
    SimpleDirectoryReader,
)
import sys
import logging
import os

os.environ["OPENAI_API_KEY"] = "INSERT YOUR KEY"


logging.basicConfig(
    stream=sys.stdout, level=logging.INFO
)  # logging.DEBUG for more verbose output


# Prepare SPARQL store  as Graph Store


# Persist
# persist KG Index(Only MetaData will be persisted, KG is in NebulaGraph)
kg_index.storage_context.persist(persist_dir='./storage_graph')
