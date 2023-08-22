# GraphRAG with SPARQL

**Status 2023-08-22:** local environment set up for experimentation, initial spike plan drawn up (below)

I reckon there's enormous potential in wiring (bits of) the Web and [Linked Data](https://en.wikipedia.org/wiki/Linked_data) to LLMs. I found an insight into a way of doing that in this [Notebook](https://www.siwei.io/en/demos/graph-rag/) from [Wey Gu](https://siwei.io/en/). ([Note](https://github.com/danja/nlp/tree/main/GraphRAG#where-was-i) below about what I was looking at beforehand).

In there he demonstrates and compares augmenting an LLM with different data structures/query engines :

- Knowledge Graph
- Graph RAG
- Vector RAG
- Graph Vector RAG

The notebook uses the [NebulaGraph](https://www.nebula-graph.io/) graph database - "Open Source, Distributed, Scalable, Lightning Fast" (does look very interesting/useful).

For a first step towards using Linked Data in a similar fashion would be to use graphs in a [SPARQL](https://en.wikipedia.org/wiki/SPARQL) store.

A snag is that NebulaGraph uses a different paradigm for graphs than SPARQL. [NebulaGraph data model](https://docs.nebula-graph.io/3.6.0/1.introduction/2.data-model/), [RDF data model](https://www.w3.org/TR/rdf11-concepts/) (**TODO** : brief comparison).

> NebulaGraph stores data in directed property graphs. A directed property graph has a set of vertices connected by directed edges. Both vertices and edges can have properties.

In so doing I reckon he's also done the groundwork for applying the same approach to Linked Data and the Web. So here's my spike plan to explore :

- [x] set up suitable dev environment locally + GitHub repo (this)
- [x] run Wey Gu's notebook locally
- [ ] familiarise myself with NebulaGraph's model (have a play)
- [ ] get more familiar with RAGs (starting with re-reading the [paper](https://github.com/danja/nlp/blob/main/GraphRAG/docs/RAG-paper.pdf) more thoroughly)
- [ ] explore notebook code, looking for a way of wrapping/abstracting the graph connections
- [ ] grab a small chunk of [Wikidata RDF](https://www.wikidata.org/wiki/Wikidata:Database_download), put it in a SPARQL store
- [ ] write SPARQLy code
- [ ] connect & test

That'll do for now.

I already had [Fuseki](https://jena.apache.org/documentation/fuseki2/) SPARQL stores set up (locally and online) - it's straightforward to install.

I installed [Jupyter](https://jupyter.org/) ages ago but had started using venv since then, that messed things up initially.

I hadn't encountered NebularGraph before. That would have been straightforward to set up, if I'd remembered to RTFM rather than guessing...

I'm jotting [rough notes](https://github.com/danja/nlp/tree/main/GraphRAG/docs) as I go along, so far just the install bits. I may get around to tidying those, but now I need a change from admin.

### Useful Links

https://github.com/todomd/todo.md

https://www.nebula-graph.io/

https://pypi.org/project/sparql-client/

https://www.wikidata.org/wiki/Wikidata:Database_download

https://gpt-index.readthedocs.io/en/latest/

LangChain & LlamaIndex
"LlamaIndex provides a simple interface between LLMs and external data sources, while LangChain provides a framework for building and managing LLM-powered applications."
([source](https://www.analyticsvidhya.com/blog/2023/06/revamp-data-analysis-openai-langchain-llamaindex-for-easy-extraction/))

### Where was I?

_There's some old personal/dev history over [here](https://github.com/danja/HKMS#the-data-model)_, but since I became aware of LLMs I'm been scratching my head trying to think of how to tie these to the Web. Ok, the visible Web can be seen as mostly a very large document database. There is also a large amount of Linked Data available on it, ie. data with more structure that could potentially be tapped into.

I (typically) made the mistake at looking at the problem from the direction of RDF : "I wouldn't start from here". Thinking vaguely aropund URLs inserted at training time as shared tokens between LLMs, something, something... So I was planning to play around with this using _small_ language models, that I could train myself (SLiMs?). This did motivate me to get back to my HKMS project, which mostly involves processing a small store of interlinked short documents, perfect fodder for a _SLiM_. But...

While I still think this could have potential, there's still a fair bit of coding for me to get the relevant HKMS bits usable in its present form, plus plenty of research/building from scratch/experimentation on the language model side. Whereas Wey Gu's approach I believe offers a much more immediate way in.
