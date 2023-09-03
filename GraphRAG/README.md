# GraphRAG with SPARQL

#### Status : 2023-09-03

- `sparql.py` is now updating store with data from LlamaIndex.
- [Initial RDF model](https://github.com/danja/nlp/tree/main/GraphRAG/src/examples/rdf-sample.ttl)
- [Demo code](https://github.com/danja/nlp/blob/main/GraphRAG/src/graph-rag-sparql-minimal.py)
- llamaindex/graphstores/[sparql.py](https://github.com/danja/llama_index/blob/add-sparql/llama_index/graph_stores/sparql.py) _(my fork/branch)_
- [SPARQL endpoint](https://fuseki.hyperdata.it/#/dataset/llama_index_sparql-test/query)

```
SELECT ?s ?p ?o WHERE {
    GRAPH <http://purl.org/stuff/guardians> {
            ?s ?p ?o
        }
}
```

_Rough progress notes [blogged](https://hyperdata.it/blog/). I've also started a write-up of the [grand plan](goal.md) (not really so grand, but I reckon has potential)_

### Description

I reckon there's enormous potential in wiring the Web and [Linked Data](https://en.wikipedia.org/wiki/Linked_data) to LLMs.

I found a wonderful insight into a promising way of doing that in this [Notebook](https://www.siwei.io/en/demos/graph-rag/), in which [Wey Gu](https://siwei.io/en/) demonstrates and compares augmenting an LLM with different data structures/query engines :

- Knowledge Graph
- Graph RAG
- Vector RAG
- Graph Vector RAG

The notebook uses the [NebulaGraph](https://www.nebula-graph.io/) graph database - "Open Source, Distributed, Scalable, Lightning Fast" (is interesting, looks useful).

A first step towards using Linked Data in a similar fashion would be to use graphs in a [SPARQL](https://en.wikipedia.org/wiki/SPARQL) store.

## Plan

_This needs tweaking a bit - later_

### Milestone 1 : recreate Notebook with SPARQL store graph

- [x] set up suitable dev environment locally + GitHub repo (this)
- [x] run Wey Gu's notebook locally
- [x] have a look at NebulaGraph's model (have a play)
- [ ] write `llama_index/graph_stores/sparql.py` **1.1**
- [ ] connect & test _(is connecting for update)_

#### 1.1

_rough progress notes [blogged](https://hyperdata.it/blog/)_

- [x] explore under `llama_index/graph_stores/`
- [x] make skeleton code for `sparql.py` (half-done already in `llama_index/graph_stores/simple.py`)
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

no! - https://pypi.org/project/sparql-client/

https://www.wikidata.org/wiki/Wikidata:Database_download

https://gpt-index.readthedocs.io/en/latest/

LangChain & LlamaIndex
"LlamaIndex provides a simple interface between LLMs and external data sources, while LangChain provides a framework for building and managing LLM-powered applications."
([source](https://www.analyticsvidhya.com/blog/2023/06/revamp-data-analysis-openai-langchain-llamaindex-for-easy-extraction/))
