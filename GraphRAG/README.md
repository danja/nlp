# GraphRAG

I reckon there's enormous potential in wiring (bits of) the Web to LLMs. I found an insight into a way of doing that in this [Notebook](https://www.siwei.io/en/demos/graph-rag/) from [Wey Gu](https://siwei.io/en/).

These different query engines :

- Knowledge Graph
- Graph RAG
- Vector RAG
- Graph Vector RAG

RAG + LLM and Knowledge Graph a

In that he augments a

QueryEngine query engine query engine Vector RAG query engine Graph Vector RAG query engine
Mechanism 1. Text-to-GraphQuery based on KG 2. Query KG with the result 3. Answer synthesis based on query result 1. Get related entities of the question 2. Get n-depth SubGraphs of related entities from KG 3. Answer synthesis based on related SubGraphs 1. Create embedding of question 2. Semantic search top-k related doc chunks 3. Answer synthesis based on related doc chunks 1. Do retrieval as Vector and Graph RAG 2. Answer synthesis based on both related chunks and SubGraphs

that should be doable, hopefully

https://www.nebula-graph.io/

https://pypi.org/project/sparql-client/

https://www.wikidata.org/wiki/Wikidata:Database_download

https://gpt-index.readthedocs.io/en/latest/

LangChain & LlamaIndex
"LlamaIndex provides a simple interface between LLMs and external data sources, while LangChain provides a framework for building and managing LLM-powered applications."
([source](https://www.analyticsvidhya.com/blog/2023/06/revamp-data-analysis-openai-langchain-llamaindex-for-easy-extraction/))
