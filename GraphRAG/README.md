# GraphRAG with SPARQL

### Status

- **2023-08-22:** local environment set up for experimentation; initial spike plan drawn up
- **2023-08-24:** some exploration; plan revised (below); started coding, nothing to see yet - rough notes in [devlog_00.md](docs/devlog_00.md)

I reckon there's enormous potential in wiring (bits of) the Web and [Linked Data](https://en.wikipedia.org/wiki/Linked_data) to LLMs. I found a wonderful insight into a promising way of doing that in this [Notebook](https://www.siwei.io/en/demos/graph-rag/), in which [Wey Gu](https://siwei.io/en/) demonstrates and compares augmenting an LLM with different data structures/query engines :

- Knowledge Graph
- Graph RAG
- Vector RAG
- Graph Vector RAG

The notebook uses the [NebulaGraph](https://www.nebula-graph.io/) graph database - "Open Source, Distributed, Scalable, Lightning Fast" (is interesting, looks useful).

A first step towards using Linked Data in a similar fashion would be to use graphs in a [SPARQL](https://en.wikipedia.org/wiki/SPARQL) store.

**Old:**

> A snag is that NebulaGraph uses a different paradigm for graphs than SPARQL. [NebulaGraph data model](https://docs.nebula-graph.io/3.6.0/1.introduction/2.data-model/), [RDF data model](https://www.w3.org/TR/rdf11-concepts/). NebulaGraph stores data in directed property graphs. A directed property graph has a set of vertices connected by directed edges. Both vertices and edges can have properties. (**TODO** : brief comparison).

**New:**

> A snag is that llama_index uses a different paradigm for graphs than SPARQL. It looks to be a 3-tuple of strings (with a schema?). (**TODO** : brief comparison)

Below I'd written a [spike](http://www.extremeprogramming.org/rules/spike.html) plan - which kinda worked as intended, as about half-way through I got a much clearer idea of what I needed to do. So while it's still exploratory, I think the following should be about the right direction to take :

## Plan

### Milestone 1 : recreate Notebook with SPARQL store graph

- [x] set up suitable dev environment locally + GitHub repo (this)
- [x] run Wey Gu's notebook locally
- [x] have a look at NebulaGraph's model (have a play)
- [ ] write `llama_index/graph_stores/sparql.py` **1.1**
- [ ] connect & test

#### 1.1

_progress notes in [devlog_00.md](docs/devlog_00.md)_

- [x] explore under `llama_index/graph_stores/`
- [ ] make skeleton code for `sparql.py` (half-done already in `llama_index/graph_stores/simple.py`)
- [ ] 10 write test for function
- [ ] 20 implement function
- [ ] 30 test, fix
- [ ] 40 GOTO 10
- [ ] tidy, document, play, look at submitting to llama_index

### Milestone : apply techniques in Notebook to existing RDF data

The RDF data I'll be using in the above will be shaped to replicate with what Wey Gu has in his notebook, with a SPARQL service as graph store. But for `sparql.py` to work with arbitrary Linked Data sources it'll likely need a fair amount of modification/extension. So this a spike to look at that:

- [ ] grab a tiny subgraph of [Wikidata RDF](https://www.wikidata.org/wiki/Wikidata:Database_download), put it in a SPARQL store
- [ ] modify/add code as necessary for llama_index to be able to consume it

That'll do for now.

#### Before

I already had [Fuseki](https://jena.apache.org/documentation/fuseki2/) SPARQL stores set up (locally and online) _it's straightforward to install_

I installed [Jupyter](https://jupyter.org/) ages ago but had started using venv since then, that messed things up initially.

I hadn't encountered NebularGraph before. That would have been straightforward to set up, if I'd remembered to RTFM rather than guessing...

I'm jotting [rough notes](https://github.com/danja/nlp/tree/main/GraphRAG/docs) as I go along. I may get around to tidying those.

#### After

I should look at the points Wey Gu makes in the notebooks conclusion :

**For those tasks:**

- Potentially cares more relationed knowledge
- Schema of the KG is sophisticated to be hard for text2cypher to express the task
- KG quality isn't good enough
- Multiple "starting entities" are involved

**Graph RAG could be a better approach to start with.**

### Potentially Useful Links

https://github.com/todomd/todo.md

https://www.nebula-graph.io/

https://pypi.org/project/sparql-client/

https://www.wikidata.org/wiki/Wikidata:Database_download

https://gpt-index.readthedocs.io/en/latest/

LangChain & LlamaIndex
"LlamaIndex provides a simple interface between LLMs and external data sources, while LangChain provides a framework for building and managing LLM-powered applications."
([source](https://www.analyticsvidhya.com/blog/2023/06/revamp-data-analysis-openai-langchain-llamaindex-for-easy-extraction/))

### Where was I?

I'm dropping everything else to crack on with the above, below is just a reminder to myself about what was on my mind previously (and gratuitous self promotion).

Since I became aware of LLMs I'm been scratching my head trying to think of how to tie these to the Web. Ok, the visible Web can be seen as mostly a very large document database. There is also a large amount of Linked Data available on it, ie. data with more structure that could potentially be tapped into.

I (typically) made the mistake at looking at the problem from the direction of RDF : "I wouldn't start from here". Thinking vaguely aropund URLs inserted at training time as shared tokens between LLMs, something, something... So I was planning to play around with this using _small_ language models, that I could train myself (SLiMs?). This did motivate me to get back to my [Hyperdata Knowledge Management System](https://hyperdata.it/hkms/) project, which mostly involves processing a SPARQL store of semantically interlinked short documents, perfect fodder for a _SLiM_. But...

While I still think this could have potential, there's still a fair bit of coding for me to get the relevant HKMS bits usable in its present form, plus plenty of research/building from scratch/experimentation on the language model side. Whereas Wey Gu's approach I believe offers a much more immediate way in.

Elsewhere I also have a long duration project intermittently in progress that uses machine learning, but that's much more on the signals side of things ([ELFQuake](https://elfquake.wordpress.com/current-design/), aiming to predict _some_ earthquakes). There's some old personal/dev history over [here](https://github.com/danja/HKMS#the-data-model). [My homepage](https://hyperdata.it/).
