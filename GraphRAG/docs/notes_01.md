**2023-08-22**

The notebook was mostly working before, but the final comparison failed. I thought it was something silly I'd done, but, going back to :

sudo /usr/local/nebula/scripts/nebula.service start all
[WARN] The maximum files allowed to open might be too few: 1024

Wey Gu explained

It's from the `ulimit -n` system call in -

```
# Perform some environment checking
function env_check {
    local nfile=$(ulimit -n 2>/dev/null)
    local core=$(ulimit -c 2>/dev/null)
    local cputime=$(ulimit -t 2>/dev/null)
```

https://github.com/vesoft-inc/nebula-graph/blob/5368115dbb67dc9e7e343cbf7388e4df3c3e1170/scripts/utils.sh#L134

sudo nano /etc/security/limits.conf

// 32768

trying -

root soft nofile 8192
root hard nofile 65536

rebooted, then

$ sudo /usr/local/nebula/scripts/nebula.service stop all
$ sudo /usr/local/nebula/scripts/nebula.service start all

no warning, and the comparison code block worked!

### looking at code

Straight to 2. Build the Knowledge Graph

documents is a big plain text block in json with a little bit of meta

next function, hmm... looking at what's in the store might help

```
NebulaGraph Studio (Studio for short) is a web-based visualization tool for NebulaGraph. With Studio, you can create a graph schema, import data, edit nGQL statements for data queries, and explore graphs in one stop.
```

(there's also Explorer for visualization, but that appears pay-for)

https://www.nebula-graph.io/download

sudo dpkg -i nebula-graph-studio-3.7.0.x86_64.deb

https://docs.nebula-graph.io/3.6.0/nebula-studio/deploy-connect/st-ug-deploy/

http://localhost:7001/ in browser

login
root:password

(used $ ./nebula-console -addr 127.0.0.1 -port 9669 -u root -p password earlier)

Tag entity 233
Edge relationship 706

Need to do a few queries...
