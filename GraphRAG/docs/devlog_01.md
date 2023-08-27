[previous devlog](devlog_00.md)

**2023-08-26**

#### Cursor Play

Last night I started playing with with https://www.cursor.so/

It's a code assistant built on VSCode (the vanilla version of which I'm already using) with calls to OpenAI API. It's free (not open source) and if you give it your API key it'll use that, rather than their billing.

Looks promising, not really there yet. Minimal docs, flaky UI. I got very confused. I'd seen it could index the whole workspace, but I didn't really want that, llama_index is pretty big and if it's hitting ChatGPT with tokens from that, the context I need will soon be lost. But it started doing it anyway...

I got as far as it sketching some functions in `sparql.py`, starting from the `types.py` interface. It tried. While it put SPARQL-ish queries in there, no way this'll run without massive modification.

Taking a different angle, I then tried to get it to make tests for nebulagraph.py.
Ended up doing that inside a copy of nebulagraph.py (not clear how to do it elsewhere). No way these will run either.

So Cursor wasn't magic. But the bits it's given me, despite being very broken, look like they'll help as a starting point/give me some clues as to what I have to do.

I've very little OpenAI API credit left, no money to top it up for a week or so, I'd better save what I have.

So back to regular VSCode with ChatGPT 4 on my other monitor. (ChatGPT credit runs out in a week as well, but that's not dependent on usage).

I haven't had a proper look at Code Interpreter yet, so once I've done a little tidying in what Cursor gave me I'll see what that can do here.

[continues here](https://hyperdata.it/blog/)
