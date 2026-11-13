# Brief changes held back while the benchmark runs

The task brief is frozen from wave 1 onward so that every run in this benchmark reads the
same text. Facts the agents reported as missing are collected here for the next version.
None has been added to TASK.md yet, and none has been checked in the lab yet unless marked.

- Dust signal strength drops by 1 per dust (w1-fable-b).
- A comparator fed 15 from behind still outputs unless its side input is also a full 15; side dust that has decayed is weaker than the back (w1-fable-b, w1-opus-b).
- A strongly powered block powers dust directly below it (w1-fable-b).
- A note block's `powered` state follows a weakly powered neighbour without conducting, so it can be an observer target (w1-fable-b).
- An observer changing state gives no block update to its side neighbours (w1-fable-b).
- An observer fires when a repeater next to it becomes locked (w1-opus-b).
- Dust on an east- or west-facing piston pops off when the piston extends (w1-opus-a).
- How an observer behaves when its watched block changes several times within a few ticks (w1-opus-a).
- A comparator may miss a 2-tick pulse fed from a repeater, but not from dust (w1-sonnet-a).
- Observers can watch observers; observer chains make good wires (w1-sonnet-b).
- `./pd py` keeps imported modules; edited helper files need `./pd py --reset` (w1-sonnet-a, w1-sonnet-b).
- Repeater and comparator `facing` names the input side, which is easy to get backwards (w1-sonnet-a, w1-sonnet-b).
- Dust connects to a redstone block and to a target block (w1-fable-a).
- A piston switched only through the cell above it ignores an observer (or a block it powers) changing; it needs dust or a moved block next to it (w1-fable-a; consistent with the update rule the brief states).
- A piston whose block lands on it one tick after its power arrives does not retry; a pulse that starts one tick late pulls the block back (w1-fable-a).
- `./pd py` output carries no "time left" line; only server tool replies do (w1-fable-a).
- A step down from dust sitting on a piston carries no power, like glass (w1-fable-a).
- A redstone block two above a piston, or beside the cell above it, switches it during settling (w1-fable-a; consistent with the brief's quasi-connectivity rule).
- The lever is not counted, so it can sit off-plane (z = 1) attached to a z = 0 block; legal as written, worth stating (w1-fable-a).
- "Within 24 blocks of the doorway" is not exact: the region is x and y from n//2-24 to n//2+23 and z from -24 to 23 (w2-4x4-opus-a).
- Slime or honey in a frame cell sticks to the hallway walls at z=±1, so any sticky structure there breaks the walls (w3-opus-d).
