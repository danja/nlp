### Coding!!

**What I need is something that does as much as :**

> NebulaGraphStore integration, for persisting graphs directly in Nebula! Furthermore, you can generate cypher queries and return natural language responses for your Nebula graphs using the KnowledgeGraphQueryEngine.

**The following are also supported, probably worth a look later :**

> Neo4j is supported as a graph store integration. You can persist, visualze, and query graphs using LlamaIndex and Neo4j. Furthermore, existing Neo4j graphs are directly supported using text2cypher and the KnowledgeGraphQueryEngine.

> We support a KuzuGraphStore integration, for persisting graphs directly in Kuzu.

**Implementation**

Something that would sit comfortably as -

llama_index/graph_stores/sparqlgraph.py

---

#### HTTP considerations

> Following the [SPARQL Protocol](https://www.w3.org/TR/sparql11-protocol/), _sparqlgraph.py_ will need to connect over HTTP. There is the [sparql-client](https://github.com/eea/sparql-client/) lib, but this only supports GET and ASK queries, no updates. The messaging is all standard, so it would be possible to use the Python http lib fairly directly, with only minimal wrappers _(I can't remember when I last did SPARQL in Python, but in other languages this has been my usual approach)_. I saw that sparql-client is based on SPARQL*JavaScript_Library by Lee Feigenbaum and Elias Torres. I've seen some of their work (met them!), so my current inclination is to start with sparql-client \_I'll have a better idea when I've seen what interfaces wil be needed.*

#### Model considerations

I'm glad I've had a little look at NebulaGraph, it eases me into what llama_index needs. But -

**little blind alley**
I've had ChatGPT 4 assisting me. Last night it made NebulaGraph queries for me :

```
USE guardians;

-- Fetch 10 vertices with the 'entity' tag
MATCH (v:entity)
RETURN v
LIMIT 10;

-- Fetch 10 edges with the 'relationship' type
MATCH (src:entity)-[e:relationship]->(dst:entity)
RETURN src, e, dst
LIMIT 10;
```

To see how far it might get, I then gave it a sample of the results, asked it to transcribe into RDF :

```
("Zune MP3 player" :entity{name: "Zune MP3 player"}) [:relationship "Zune MP3 player"->"International Space Station" @-1969550742602721981 {relationship: "launched inside"}] ("International Space Station" :entity{name: "International Space Station"})
```

=>

```
@prefix ex: <http://example.org/> .

ex:ZuneMP3Player a ex:entity ;
    ex:name "Zune MP3 player" .

ex:InternationalSpaceStation a ex:entity ;
    ex:name "International Space Station" .

ex:ZuneMP3Player ex:launchedInside ex:InternationalSpaceStation .
```

Not an unreasonable way of representing what I gave it, useless here.

I went back to the notebook. To be able to read the code more easily I exported it as a .py.

Running that failed around :

`storage_context = StorageContext.from_defaults(persist_dir='./storage_graph', graph_store=graph_store)`

That led me to noseying around the llama_index code, where I found :

```
llama_index.graph_stores
```

Which is where I should have been looking in the first place. D'oh!

**reverse out of blind alley and continue**

Under `llama_index/graph_stores` there are :

- `--init--.py` - usual namespace/packaging thing
- `types.py` - the interface for a graph store _Yay!_
- `simple.py` - a minimal graph store, backed by an in-memory dictionary _Woo-hoo!_
- `registery.py` - a dictionary of the implementations
- `nebulagraph.py` - implementation
- `neo4j.py` - implementation
- `kuzu.py` - implementation
- `falkordb.py` - implementation

There is a `/tests/` tree, but I couldn't see anything directly relevant to the graph stuff.

I did find `def mock_extract_triplets(text: str) -> List[Tuple[str, str, str]]:` - which may be involved in what I need...

So now to :

- copy `simple.py` to `sparql.py`
- decide on how to represent the llama_index triplets as RDF triples
- write the necessary SPARQL queries (check in the Fuseki UI client against a Fuseki store)
- figure out how to insert [sparqlwrapper](https://github.com/RDFLib/sparqlwrapper) into `sparql-client`
  ~~figure out how to insert `sparql-client` into `sparql.py`~~

Hah! I was expecting to have to extend sparql-client. Just by chance saw a post from @AndySeaborne about a new release of RDFLib, which I've not been following.
Has sparqlwrapper associated, which I think will cover the necessary.

I've no immediate need, but installing RDFLib's SPARQL server goes on the \*_TODO_, if only to have a look.

I will need to deal with things like config for endpoints etc, for now just hardcode

### Admin

**GitHub**

- forked llama_index, sparql-client
- branches add-sparql,

llama_index dir

git branch add-sparql
git checkout add-sparql

#### Docs

https://github.com/jerryjliu/llama_index/blob/main/docs/DOCS_README.md

pip install -r docs/requirements.txt

cd docs
make html

make watch-docs

**TODO**

llama_index/docs/examples/index_structs/knowledge_graph/NebulaGraphKGIndexDemo.ipynb

equiv to :

https://gpt-index.readthedocs.io/en/latest/examples/index_structs/knowledge_graph/Neo4jKGIndexDemo.html

#### Tests

pip install pytest

_pip install unittest_

> version failed - but looks like pytest covers everything anyway

**TODO**

/home/danny/AI/nlp/llama_index/tests/graph_stores/test_sparql.py

equiv to :

/home/danny/AI/nlp/llama_index/tests/vector_stores/test_cassandra.py

/home/danny/AI/nlp/llama_index/tests/vector_stores/test_postgres.py

**Implementation**

pip install sparqlwrapper

#### Later

> the `KnowledgeGraphIndex` from LlamaIndex, when creating it, Triplets will be extracted with LLM and evantually persisted into `NebulaGraphStore`.

note - /home/danny/AI/nlp/llama_index/llama_index/schema.py
