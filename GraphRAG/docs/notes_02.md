**2023-08-23**

nGQL to explore data, get ChatGPT 4 to help

Prompts :

```
You are a graph database expert. Your responses will be just the requested code, with at most a single sentence of explanation
```

```
in a NebulaGraph database, there is a single graph space named 'guardians'.  The schema has a single tag named 'entity', a single edge named 'relationship', a single index named entity_index. Create a nGQL query to show some sample data to help me visualise this (at most 10 results)
```

response:

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

using Console in NebulaGraph Studio (tweaked limit to see other bits)

MATCH (v:entity)
RETURN v
LIMIT 1000;

results include :

("$118.4 million" :entity{name: "$118.4 million"})
("$168.1 million in its opening weekend" :entity{name: "$168.1 million in its opening weekend"})
...
("Orgocorp" :entity{name: "Orgocorp"})
("Orgocorp's headquarters" :entity{name: "Orgocorp's headquarters"})
("Peter Quill" :entity{name: "Peter Quill"})
("Philz" :entity{name: "Philz"})

Yay! Has a graph view!

MATCH (src:entity)-[e:relationship]->(dst:entity)
RETURN src, e, dst
LIMIT 1000;

("Zune MP3 player" :entity{name: "Zune MP3 player"}) [:relationship "Zune MP3 player"->"International Space Station" @-1969550742602721981 {relationship: "launched inside"}] ("International Space Station" :entity{name: "International Space Station"})

("Zune MP3 player" :entity{name: "Zune MP3 player"}) [:relationship "Zune MP3 player"->"International Space Station" @862072256707230213 {relationship: "launched inside"}] ("International Space Station" :entity{name: "International Space Station"})
...
("Braham" :entity{name: "Braham"}) [:relationship "Braham"->"cinematographer" @9080478547192331685 {relationship: "serves as"}] ("cinematographer" :entity{name: "cinematographer"})

("Adam" :entity{name: "Adam"}) [:relationship "Adam"->"Ayesha" @3271216664970418415 {relationship: "is created by"}] ("Ayesha" :entity{name: "Ayesha"})

("A second trailer for the film" :entity{name: "A second trailer for the film"}) [:relationship "A second trailer for the film"->"2023" @-6195836530402655361 {relationship: "released during Super Bowl LVII on February 12"}] ("2023" :entity{name: "2023"})

("A second trailer for the film" :entity{name: "A second trailer for the film"}) [:relationship "A second trailer for the film"->"2023" @-2065708856721800391 {relationship: "released during Super Bowl LVII on February 12"}] ("2023" :entity{name: "2023"})

("A second trailer for the film" :entity{name: "A second trailer for the film"}) [:relationship "A second trailer for the film"->"2023" @2591341498553255806 {relationship: "released during Super Bowl LVII on February 12"}] ("2023" :entity{name: "2023"})
