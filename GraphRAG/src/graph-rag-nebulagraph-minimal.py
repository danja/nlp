# local prep
# sudo /usr/local/nebula/scripts/nebula.service start all
# export PYTHONPATH=$PYTHONPATH:/home/danny/AI/LIBS-under-dev/llama_index

# from 1.1 Prepare for LLM & Azure
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
from llama_index.graph_stores import NebulaGraphStore
from llama_index.llms import OpenAI
from IPython.display import Markdown, display
from llama_index import load_index_from_storage
import os
import sys

# is safe, revoked
os.environ["OPENAI_API_KEY"] = "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"


logging.basicConfig(
    stream=sys.stdout, level=logging.INFO
)  # logging.DEBUG for more verbose output

# ----
# from 1.2. Prepare for NebulaGraph as Graph Store


os.environ['NEBULA_USER'] = "root"
os.environ['NEBULA_PASSWORD'] = "nebula"  # default password
# assumed we have NebulaGraph installed locally
os.environ['NEBULA_ADDRESS'] = "127.0.0.1:9669"

space_name = "guardians"
# default, could be omit if create from an empty kg
edge_types, rel_prop_names = ["relationship"], ["relationship"]
tags = ["entity"]  # default, could be omit if create from an empty kg

graph_store = NebulaGraphStore(
    space_name=space_name,
    edge_types=edge_types,
    rel_prop_names=rel_prop_names,
    tags=tags,
)
storage_context = StorageContext.from_defaults(graph_store=graph_store)

# ----
# skip 2...
# ----
# from 3 Create VectorStoreIndex for RAG
# wants the original documuments
# vector_index = VectorStoreIndex.from_documents(
#    documents,
#    service_context=service_context
# )

# ----
# this bit appeared earlier, service_context is asked for, hopefully not need below
llm = OpenAI(temperature=0, model="text-davinci-002")
service_context = ServiceContext.from_defaults(llm=llm, chunk_size=512)

# ----
# from 4. Persist and Load from disk Llama Indexes(Optional)

# vector_index.storage_context.persist(persist_dir='./storage_vector')

storage_context = StorageContext.from_defaults(
    persist_dir='./storage_graph', graph_store=graph_store)
kg_index = load_index_from_storage(
    storage_context=storage_context,
    service_context=service_context,
    max_triplets_per_chunk=10,
    space_name=space_name,
    edge_types=edge_types,
    rel_prop_names=rel_prop_names,
    tags=tags,
    include_embeddings=True,
)

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
# from 5.1 text-to-NebulaGraphCypher

nl2kg_query_engine = KnowledgeGraphQueryEngine(
    storage_context=storage_context,
    service_context=service_context,
    llm=llm,
    verbose=True,
)

# ----
# from 5.2 Graph RAG query engine
kg_rag_query_engine = kg_index.as_query_engine(
    include_text=False,
    retriever_mode="keyword",
    response_mode="tree_summarize",
)

# ----
# 5.3 Vector RAG query engine
vector_rag_query_engine = vector_index.as_query_engine()

# ----
# 6.1 Text-to-GraphQuery

# response_nl2kg = nl2kg_query_engine.query("Tell me about Peter Quill.")
# calls OpenAI

# display(Markdown(f"<b>{response_nl2kg}</b>"))

# Cypher:

# print("Cypher Query:")

# graph_query = nl2kg_query_engine.generate_query(
#    "Tell me about Peter Quill?",
# )
# calls OpenAI

# graph_query = graph_query.replace(
#    "WHERE", "\n  WHERE").replace("RETURN", "\nRETURN")

# display(
#    Markdown(
#        f"""
# ```cypher
# {graph_query}
# ```
# """
#    )
# )

# ----
# 6.2 Graph RAG

# response_graph_rag = kg_rag_query_engine.query("Tell me about Peter Quill.")

# display(Markdown(f"<b>{response_graph_rag}</b>"))
