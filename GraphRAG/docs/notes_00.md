**2023-08-19**

Start with running the demo locally

$ cd AI/graphRAG

downloaded https://www.siwei.io/en/demos/graph-rag/

$ jupyter notebook

added OpenAI API key

https://platform.openai.com/account/api-keys

another shell (should have &-ed?)

oof, forgotten, I set Python up for venv since last using Jupyter locally

[[[[ -----------------------------------------NO!
$ python3 -m venv ./

$ bin/pip install llama_index

$ bin/pip install nebula3-python ipython-ngql
]]]]

no.

sudo apt-install pipx

$ pipx install llama_index
$ pipx install nebula3-python ipython-ngql
]]]
no!!
------------------------------------------------END NO!

turn off venv :

sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/_EXTERNALLY-MANAGED_

$ pip3 install llama-index
$ pip3 install nebula3-python ipython-ngql

[[
https://docs.nebula-graph.io/2.0/2.quick-start/0.FAQ/

Does Nebula Graph support W3C RDF (or SPARQL, GraphQL)?¶
No.

Nebula Graph's data model is the property graph, and it is a strong schema system.

It doesn't support rdf.

Nebula Graph Query Language does not support SPARQL nor GraphQL.
]]

https://www.nebula-graph.io/download
downloaded NebulaGraph DB v3.6.0

https://docs.nebula-graph.io/3.6.0/2.quick-start/2.install-nebula-graph/

sudo dpkg -i nebula-graph-3.6.0.ubuntu2004.amd64.deb

sudo /usr/local/nebula/scripts/nebula.service start
Usage: /usr/local/nebula/scripts/nebula.service [-v] [-c /path/to/config] <start|stop|restart|status|kill> <metad|graphd|storaged|all>

^^^ need to specify the services

danny@danny-desktop:~/Downloads$ sudo /usr/local/nebula/scripts/nebula.service start all
[WARN] The maximum files allowed to open might be too few: 1024
[INFO] Starting nebula-metad...
[INFO] Done
[INFO] Starting nebula-graphd...
[INFO] Done
[INFO] Starting nebula-storaged...
[INFO] Done

downloaded nebula-console

https://github.com/vesoft-inc/nebula-console/releases

NebulaGraph Console v3.5.0

[good-o, @wey-gu is a dev on NebulaGraph]

chmod 111 nebula-console

./nebula-console

2023/08/19 22:45:18 Error: argument port is missed!

Oops...

danny@danny-desktop:~/AI/graphRAG$ sudo /usr/local/nebula/scripts/nebula.service status graphd
[sudo] password for danny:
[WARN] The maximum files allowed to open might be too few: 1024
[INFO] nebula-graphd(de9b3ed): Running as 12147, Listening on 9669

...more mistakes due to missing bits - RTFM...

https://docs.nebula-graph.io/3.6.0/2.quick-start/3.connect-to-nebula-graph/

$ ./nebula-console -addr <ip> -port <port> -u <username> -p <password>
[-t 120] [-e "nGQL_statement" | -f filename.nGQL]

danny@danny-desktop:~/AI/graphRAG$ ./nebula-console -addr 127.0.0.1 -port 9669 -u root -p password

Welcome!

(root@nebula) [(none)]>

....

(root@nebula) [(none)]> CREATE SPACE guardians(vid_type=FIXED_STRING(256), partition_num=1, replica_factor=1);
[ERROR (-1005)]: Host not enough!

---

back up ^^^

maybe :
[WARN] The maximum files allowed to open might be too few: 1024

sudo /usr/local/nebula/scripts/nebula.service stop all

-c Specify the configuration file path. The default path is /usr/local/nebula/etc/.

sudo /usr/local/nebula/scripts/nebula.service stop graphd

ls /usr/local/nebula/etc/

nebula-graphd.conf  
 nebula-graphd.conf.default
nebula-graphd.conf.production

can't see a ref to files. RTFM again

https://docs.nebula-graph.io/3.6.0/4.deployment-and-installation/manage-storage-host/

Ah. Need to make some storage exist, then tell it about the storage. That'll be metad and storaged

services

$ sudo /usr/local/nebula/scripts/nebula.service start all

console

$ ./nebula-console -addr 127.0.0.1 -port 9669 -u root -p password

Make sure that the IP address and port number are the same as those in the configuration file. For example, the default IP address and port number in standalone deployment are 127.0.0.1:9779.

nebula> ADD HOSTS 127.0.0.1:9779;

Try the Graph RAG script again -

YAY! all "Execution succeeded"

back to notebook
...a little later, got a fresh copy

Removed blocks

# For Azure OpenAI

# vector_index.storage_context.persist(persist_dir='./storage_vector')

this time, 2.2 Extract Triplets and Save to NebulaGraph failed with an auth error (I've sure it worked last time)

$ sudo /usr/local/nebula/scripts/nebula.service restart all

INFO:openai:error_code=insufficient_quota error_message='You exceeded your current quota, please check your plan and billing details.
