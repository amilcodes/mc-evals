# Task: the smallest working 2x2 piston door

Design a redstone piston door for Minecraft Java Edition 26.3 (unmodified game rules) and make
it as small as you can. 26.3 is a 2026 release; its redstone and pistons follow the
long-standing Java Edition rules, with the experimental redstone changes switched off. A grader builds your design in the real game engine, operates it,
and measures it. You have tools to test designs and to watch what they do tick by tick.

Your score is based on the **volume of the bounding box** of your final design, provided it
passes every rule below. A design that breaks a rule scores zero, so a working door comes
first and a smaller one second.

## The world

Coordinates are relative to the doorway. +x is east, +y is up, +z is south (north is -z).

- **Doorway:** the 2x2 cells `(x, y, 0)` with `0 <= x <= 1` and `0 <= y <= 1`.
- **Hallway:** the same 2x2 column at every other z. It runs straight through the doorway
  in both directions and must stay empty at all times.
- **Hallway walls:** a tube of stone, one block thick, wraps the hallway at every `z != 0`.
  It is the cells touching the hallway: `x = -1` or `x = 2` with `0 <= y <= 1`, and
  `y = -1` or `y = 2` with `0 <= x <= 1`. The grader places it before your design. These
  blocks are not yours: you may not place anything there, and nothing may move or replace
  them. They do not count toward your size. They are ordinary stone, so they conduct
  redstone power, can support dust placed on top of them, and can have the lever attached.
- The four diagonal corner columns, such as `(-1, -1, z)` and `(2, 2, z)`, are not walls. They are air and yours to use.
  The two upper ones have wall stone directly beneath them, so dust can run along them.
- **Everything else is empty air and yours to build in, at every z.** That includes the whole
  z = 0 layer around the doorway and everything outside the tube in front of and behind it
  (for example `(-2, 0, 1)` or `(0, 3, -1)`), so wiring can run in three dimensions. Blocks
  do not need support unless the block itself requires it (dust, torches and levers do).
- You may build anywhere within 24 blocks of the doorway.

The door is **closed** when all 4 doorway cells hold `stone`, and **open** when all 4 are air.

**Track: seamless.** Whenever the build is at rest, every cell that shares a face with an *empty* doorway
cell must hold a plain block (see the allowed-blocks list; redstone components, glass and air are not plain).
In practice: with the door open, the 8 frame cells directly left, right, above and below the doorway, in
the z = 0 layer, must be plain blocks, so that someone standing in the hallway sees only ordinary blocks.
When the door is closed the doorway is full, so nothing behind it is checked. Movement in between is not checked.

## What you submit

A design is JSON:

```json
{"initial_state": "open",
 "blocks": [
  {"pos": [-3, -1, 0], "id": "stone"},
  {"pos": [-3, 0, 0], "id": "lever", "props": {"face": "floor", "facing": "north"}},
  {"pos": [-2, 0, 0], "id": "sticky_piston", "props": {"facing": "east"}},
  {"pos": [-1, 0, 0], "id": "stone"}
 ]}
```

This example is a complete one-cell door (a 1x1, shown only to illustrate the format): a
lever beside a sticky piston that pushes one stone block east into the cell `(0, 0, 0)`.

- `initial_state` says whether the door starts `open` or `closed`. If it starts closed, the
  doorway cells must contain `stone` in your block list. If it starts open, your block list
  must leave them empty.
- Exactly one `lever`, switched off. It is the only input. Each flip of the lever must
  toggle the door. Which lever position means open is up to you.
- Only blocks from the allow-list. Properties you leave out take the game's defaults.
  Leave out redstone dust's shape and power; the game works them out (one exception is
  noted under component facts).
- If a piston starts extended you must also list its `piston_head` in the cell in front of it.

## How a design is tested

1. **Checked** against the format and placement rules. Problems are reported with positions
   and this does not use up a test.
2. **Placed and settled.** All blocks appear at once, then every block receives one update.
   The build must stop changing within 40 ticks and the doorway must match `initial_state`.
   A block that cannot exist where you put it (dust with nothing under it) disappears, and
   you get a note. The same note appears, harmlessly, when a piston moves a block during settling. Anything the placement update sets off, such as a lit torch powering
   a piston, plays out here, before the first lever flip. `initial_state` is checked afterwards.
3. **Cycled** several times. After each lever flip the doorway must reach the other state
   within **200 game ticks** (20 ticks = 1 second), the whole build must come to rest (no block
   changing for 20 ticks, so no free-running clocks), and it must then stay unchanged for
   40 more ticks.
4. **On every tick, including while parts are moving:** no entities may appear (a dropped
   item counts, for example dust whose support was pulled away), the hallway must stay
   empty, and the hallway walls must not change.

Your final design gets one stricter test with more cycles and flips at varied moments
after the build has come to rest. Flips never arrive while it is still moving.

## Size

Volume = width x height x depth of the smallest box containing every cell one of your
blocks occupied at any moment (including blocks in motion and extended piston heads),
plus the doorway itself.

- Every block you place counts, including plain frame blocks around the doorway.
- The lever is not counted: its cell is ignored even if it lies outside the box of everything else.
- The grader's hallway walls are not counted.

## Component facts for this game version

These were checked in the grader's own simulator.

- A piston's `facing` is the direction its head extends. Pistons push at most 12 blocks.
  Sticky pistons pull the block in front back when they retract. Obsidian cannot be moved.
- An observer's `facing` is the direction it watches. It emits a short pulse from the opposite side.
- A repeater or comparator's `facing` is the side its **input** comes from; the output leaves
  from the opposite side. Example: with a lever to the west and dust to the east, use `facing=west`.
- A `redstone_wall_torch`'s `facing` points away from the block it hangs on; that block is on
  the opposite side. A `redstone_torch` stands on the block below it.
- A lever with `face=floor` stands on the block below, `face=ceiling` hangs from the block
  above, and with `face=wall` it is attached to the block on the side opposite its `facing`.
  A lever powers the block it is attached to and any component next to it.
- Redstone dust needs a block under it: any solid block, and also glass, a slime block, a
  redstone block, the top of an observer, or a piston (checked facing north, up and down).
  Glass and observers also hold repeaters.
- Dust connects to dust beside it, to the front or back of a repeater, to the side of a
  comparator, and to the back of an observer. It does not connect to pistons.
- Dust also connects to dust one block up or down on a neighbouring block, unless the cell
  above the lower dust holds a block that cuts the step. Of the allowed blocks, glass, honey,
  observers, pistons and redstone blocks do not cut it (observers and pistons checked facing
  north); every other full block does.
- A step down from dust on glass connects but carries no power: the lower dust stays
  unpowered. Power does go up a step onto dust on glass, so a glass staircase carries a
  signal up but not down.
- Dust with a single connection also points out of the opposite side. Dust with no
  connection is a dot, unless you list all four of its sides as `side`, which makes a cross
  that points all four ways. The cross lasts only while nothing connects to the dust: as
  soon as anything does, including dust one step up or down, the game recomputes the shape,
  and one connection makes a line. Otherwise leave dust's shape out.
- Powered dust powers the block underneath it and whatever it points at. It does not power
  a block or piston beside it that it does not point at, and a dot powers only the block
  underneath. A piston beside dust is powered only if the dust is a line aimed at it.
- Glass and observers do not pass power on. A piston beside a glass block or an observer
  with powered dust on top stays put; beside a stone it would move (observer checked facing
  east and up).
- Quasi-connectivity: a piston is also switched by anything that would power the cell
  directly above it: a powered block next to that cell, including one above it (two above
  the piston), or dust aimed into the cell or sitting on top of it. But a piston only
  rechecks its power when it gets a block update. Dust changing power within two blocks of
  the piston gives it one (checked two straight up, and one up and one across). A lever on a
  block beside the cell above, or on a block two above the piston, does not: the piston
  stays as it was until a block next to it changes, and then moves. Check for this whenever
  wiring passes near the cell above a piston.
- A piston cannot push an extended piston. Repeaters accept `powered` and `delay`; a
  repeater placed `powered=true` with no input switches off after its delay.
- A repeater can take its input straight from an observer's back, or from a block that a
  lever powers. A comparator's side input reads dust beside it: in subtract mode, side dust
  at strength 15 switched off a comparator fed 15 from behind.
- An observer watching a piston fires once when the piston extends and once when it retracts.
- Java Edition short-pulse piston behaviour applies (see the timings below).

Timings, in the ticks the `trace` tool reports (the lever flips at t=0):

- A piston powered straight from the lever, from dust or from a powered block starts moving
  at t=1 and has finished at t=3. Retracting takes the same two ticks. Further down a
  circuit, when a repeater or observer switches dust on at tick t, a piston on that dust
  starts moving at the same t and has finished at t+2.
- A repeater adds 2 ticks per delay step, and stretches a pulse shorter than its delay to
  the length of its delay. A comparator adds 2. A torch switches 2 ticks after the block it
  is on changes.
- An observer turns on 2 ticks after the change it sees and off 2 ticks later. A sticky
  piston given that 2-tick pulse pushes its block and leaves it behind; the next pulse
  fetches it back.
- A piston that another piston pushes into a powered position (for example beside a
  redstone block) starts its own stroke the tick after it lands and has finished two ticks
  later.
- Observers do not fire merely for being placed. They fire when the cell they watch changes,
  which includes changes during settling.

## Tools

Run these from this folder.

| Command | What it does |
|---|---|
| `./pd status` | Task, remaining budget, best result so far |
| `./pd blocks` | Allowed blocks and their properties |
| `./pd test design.json` | The full test: valid or not, why not, volume, timings |
| `./pd trace design.json [--flips N] [--ticks T] [--grep TEXT] [--limit L]` | Every block change, tick by tick, after placement and after each flip |
| `./pd view design.json [--flips N] [--z A..B]` | ASCII picture of the build, one grid per z layer |
| `./pd submit design.json` | Nominate your final design. You can submit again; the last one counts |

In `trace` output, the first line for each flip shows the doorway's state over time
(`t0 .../.../...  t14 ###/###/###`), which is often all you need: `--limit 0` prints only
those lines. `--grep` keeps only change lines containing the text, for example `--grep "(1,4,1)"`.

`pdbuild.py` is an optional Python helper for writing designs (`from pdbuild import Design`).
`example_1x1.json` is the one-cell example above; try `./pd trace example_1x1.json` to see the output format.


## The lab

`test`, `trace` and `view` need a complete door. The lab does not. It is an empty world where
you place any set of blocks and run it one step at a time, to find out how a part behaves
before you build a door around it. A lab call returns in well under a second (about a
second for a world near the tick limit below), so it is cheap to try an idea instead of
reasoning it out.

- **Blocks.** Anything on the allow-list, anywhere within 24 blocks of the doorway, doorway
  and hallway cells included. None of the door rules apply: there may be no lever or several,
  and nothing is checked or scored. Coordinates mean the same as in a design, so a part that
  works in the lab can be put into a design unchanged.
- **Hallway walls** are absent unless you ask for them. With them, their cells cannot be used,
  as in a design.
- **Placement** is the same as in a test: every block appears at once, each receives one
  update, and observers do not fire. A block that cannot exist where you put it is removed
  and listed. Unlike a test, nothing runs afterwards: the lab clock is at t=0 and no tick has passed.
- **The clock** counts game ticks since the lab was started. It moves only when you step or
  rest; nothing happens between calls.
- **Flip** switches the lever at a position you name and takes no time. Blocks that change in
  that instant (dust, for example) are listed with the current t. A piston powered by a flip
  at t starts moving at t+1 and has finished at t+3, which matches `trace`, where the flip is t=0.
- **Step** advances exactly the number of ticks you ask for (1 to 2000) and lists every
  block change with its tick. Stepping 5 and then 3 is the same as stepping 8.
- **Rest** advances until no block has changed for 20 ticks in a row, which is the test's
  meaning of "at rest", or until a maximum you give (default 200). When it comes to rest the
  clock stands 20 ticks after the last change.
- **Look** and **view** report the current state and take no time.
- One lab world can run at most 4000 ticks in all. After that, start a new lab.
- The first item drop or falling block to appear is reported (`ENTITY appeared`); later ones are not.
- There is one lab world, and starting a new lab empties it. It is separate from the world
  `test`, `trace` and `view` use: they never disturb the lab and the lab never affects them.
- `trace` is the same thing done for you: with the hallway walls present, starting a lab with
  a complete design, then rest, flip, rest, flip, rest gives the same block changes on the
  same ticks as `trace` shows for two flips, counting from each flip.

| Command | What it does |
|---|---|
| `./pd lab new part.json [--walls]` | Empty the lab and place the blocks in the file: a design, or a bare JSON list of blocks |
| `./pd lab flip X Y Z` | Flip the lever at that position |
| `./pd lab step [N] [--grep TEXT] [--limit L]` | Advance exactly N ticks (default 1) |
| `./pd lab rest [--max N] [--grep TEXT] [--limit L]` | Advance until at rest |
| `./pd lab look [--at X Y Z]... [--grep TEXT]` | State of every block (hallway walls left out), or of the cells named (an empty cell reads `air`), and the doorway |
| `./pd lab view [--z A..B]` | ASCII picture of the lab now; it always includes the doorway cells |

### The Python session

`./pd py` runs Python in an interpreter that stays alive between calls, so variables,
functions and lab objects are still there the next time. Give it code in one of three ways:

```
./pd py -c 'part = Design()'
./pd py script.py
./pd py <<'EOF'
...several lines...
EOF
```

- It runs in this folder. `Design` and everything in `pdlab.py` are already imported.
- What the code prints comes back. If the last statement is an expression, its value is
  printed too (unless it is `None`).
- An error prints a traceback and `./pd py` exits with status 1. The session and its variables survive.
- Calls run one after another, never at the same time.
- Output beyond 30,000 characters per call is cut off, and says so.
- A call that has not finished after 300 seconds (`--timeout S` changes this) is stopped
  together with the session: every variable is lost and the next call starts a new session.
- `./pd py --reset` ends the session. A session left unused for 6 hours ends by itself.

`pdlab.py` holds the same tools as `./pd`, with the same budgets:

| Python | What it does |
|---|---|
| `lab = Lab(part, walls=False)` | Start a lab. `part` is a `Design`, a list of blocks, a design dict, or a file path. `lab.lost` lists blocks removed at placement |
| `lab.flip(x, y, z)` | Flip that lever. Returns the changes made in that instant |
| `lab.step(ticks=1)` | Advance. Returns the changes as `(t, (x, y, z), before, after)` tuples, in order |
| `lab.rest(max_ticks=200)` | Advance until at rest. Returns `True` if it came to rest |
| `lab.block(x, y, z)`, `lab.blocks()` | One cell's state (`"air"` if empty); or `{(x, y, z): state}` for every block (hallway walls left out) |
| `lab.doorway()` | The doorway as rows, top first, such as `"###/#.#/###"` (`#` stone, `.` air, `m` moving, `?` other) |
| `lab.view(z=None)` | The ASCII picture, as text |
| `lab.t`, `lab.history`, `lab.timeline(x, y, z)` | The clock; every change returned so far; the states one cell took, as `(t, state)` |
| `lab.entity` | `(t, type)` of the first entity that appeared, else `None` |
| `r = test(design)` | The full test. `r.valid`, `r.volume`, `r.dims`, `r.failures` (codes), `r.rejected`, `r.refused`, `r.text`; `print(r)` shows the report |
| `trace(design, flips=2, ticks=None, grep=None, limit=80)`, `view(design, flips=0, z=None)` | The same text as the commands |
| `submit(design)`, `status()`, `blocks()` | The same text as the commands |

A call the server refuses (rejected blocks, no lever at that position, not enough lab ticks
left) raises `PdError` with the server's message. Creating a new `Lab` empties the lab world,
so an older `Lab` object raises `PdError` from then on. `Design.translate` moves a design in
place; use `part.copy().translate(...)` to keep the original.

`example_lab.py` is a short worked example: `./pd py example_lab.py`.

## Budget

You have **150 test calls**, **400 trace/view calls** and **50000 lab ticks**. Designs
rejected in step 1 are free. In the lab only ticks advanced by step and rest count; starting
a lab, flip, look and view are free. You also have **60 minutes**, counted from your
first tool call. This is wall-clock time: thinking between calls counts too. Every tool reply ends with the time left. Once the time is up, `test`, `trace`, `view` and the lab are refused; status, the block list and submit still work.
If you never submit, your smallest design that passed a test is used.

The first design that works is rarely the smallest. The budget is there to be used: once you
have a valid door, keep looking for a smaller one until you run out of calls or of ideas.

## Ground rules

- Work only inside this folder. Do not read or change anything outside it, and do not use the internet.
- The grader's verdict is final. Do not try to interfere with it.
- Before you finish, run `./pd submit` on the design you want scored.
