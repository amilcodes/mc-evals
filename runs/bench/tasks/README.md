# Repair and physics-port tasks

Each task gives an agent a broken or mis-tuned redstone build and a spec. The agent must make the build meet the spec, and the real Minecraft 26.3 engine checks the result. Every task was verified the same way: its starting build fails, its reference fix passes, and a set of hack probes is refused.

| Family | Tasks | Repair | Port | Hidden rule | Checker |
|---|---:|---:|---:|---:|---|
| [doors](doors/) | 30 | 19 | 8 | 3 | the benchmark's own final grade, plus volume, block and edit budgets |
| [logic](logic/) | 31 | 17 | 10 | 4 | output trace, exact to the tick, over at least 3 on/off cycles |
| [pistons](pistons/) | 34 | 22 | 8 | 4 | target cells at rest after each toggle, plus clear and fixed cells |

The task kinds:

- **Repair:** a working build broken by one to four edits.
- **Port:** a build that works under one physics setting but has to be made to work under another.
- **Hidden rule:** a port where the agent is not told which setting changed.

A task is labelled **hard** when a full search of every single-block edit found no fix. Each family's README gives its format, how its tasks were made, and what its checker cannot catch.
