"""The task brief an agent reads, and the folder a command-line agent works in.

brief() renders the brief for either interface: "cli" (the `./pd` client in a working
folder) or "tools" (function-calling tools, as in the Inspect task).
"""
import json
import shutil
from pathlib import Path

from . import rules
from .session import DEFAULT_BUDGET, LAB_MAX_STEP, LAB_WORLD_TICKS

TEMPLATE = Path(__file__).resolve().parent.parent / "kit_template"

EXAMPLE = {
    "initial_state": "open",
    "blocks": [
        {"pos": [-3, -1, 0], "id": "stone"},
        {"pos": [-3, 0, 0], "id": "lever", "props": {"face": "floor", "facing": "north"}},
        {"pos": [-2, 0, 0], "id": "sticky_piston", "props": {"facing": "east"}},
        {"pos": [-1, 0, 0], "id": "stone"},
    ],
}

TRACK_RULE = {
    "open": "**Track: open.** There is no rule about what can be seen. Any door that works counts.",
    "seamless": (
        "**Track: seamless.** Whenever the build is at rest, every cell that shares a face with an *empty* doorway\n"
        "cell must hold a plain block (see the allowed-blocks list; redstone components, glass and air are not plain).\n"
        "In practice: with the door open, the {ring} frame cells directly left, right, above and below the doorway, in\n"
        "the z = 0 layer, must be plain blocks, so that someone standing in the hallway sees only ordinary blocks.\n"
        "When the door is closed the doorway is full, so nothing behind it is checked. Movement in between is not checked."
    ),
}

# Added to the doorway line for rectangular doors only, so square briefs stay as they were.
SHAPE_NOTE = (" The door is {w} cells wide (along x) and {h} cells tall (along y); it is not square, so mind"
              " which side is which.")

BRIEF = """# Task: the smallest working {w}x{h} piston door

Design a redstone piston door for Minecraft Java Edition {version} (unmodified game rules) and make
it as small as you can. {version} is a 2026 release; its redstone and pistons follow the
long-standing Java Edition rules, with the experimental redstone changes switched off. A grader builds your design in the real game engine, operates it,
and measures it. You have tools to test designs and to watch what they do tick by tick.

Your score is based on the **volume of the bounding box** of your final design, provided it
passes every rule below. A design that breaks a rule scores zero, so a working door comes
first and a smaller one second.

## The world

Coordinates are relative to the doorway. +x is east, +y is up, +z is south (north is -z).

- **Doorway:** the {w}x{h} cells `(x, y, 0)` with `0 <= x <= {mw}` and `0 <= y <= {mh}`.{shape_note}
- **Hallway:** the same {w}x{h} column at every other z. It runs straight through the doorway
  in both directions and must stay empty at all times.
- **Hallway walls:** a tube of stone, one block thick, wraps the hallway at every `z != 0`.
  It is the cells touching the hallway: `x = -1` or `x = {w}` with `0 <= y <= {mh}`, and
  `y = -1` or `y = {h}` with `0 <= x <= {mw}`. The grader places it before your design. These
  blocks are not yours: you may not place anything there, and nothing may move or replace
  them. They do not count toward your size. They are ordinary stone, so they conduct
  redstone power, can support dust placed on top of them, and can have the lever attached.
- The four diagonal corner columns, such as `(-1, -1, z)` and `({w}, {h}, z)`, are not walls. They are air and yours to use.
  The two upper ones have wall stone directly beneath them, so dust can run along them.
- **Everything else is empty air and yours to build in, at every z.** That includes the whole
  z = 0 layer around the doorway and everything outside the tube in front of and behind it
  (for example `(-2, 0, 1)` or `(0, {h1}, -1)`), so wiring can run in three dimensions. Blocks
  do not need support unless the block itself requires it (dust, torches and levers do).
- You may build anywhere within 24 blocks of the doorway.

The door is **closed** when all {cells} doorway cells hold `stone`, and **open** when all {cells} are air.

{track_rule}

## What you submit

A design is JSON:

```json
{example}
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
   The build must stop changing within {settle} ticks and the doorway must match `initial_state`.
   A block that cannot exist where you put it (dust with nothing under it) disappears, and
   you get a note. The same note appears, harmlessly, when a piston moves a block during settling. Anything the placement update sets off, such as a lit torch powering
   a piston, plays out here, before the first lever flip. `initial_state` is checked afterwards.
3. **Cycled** several times. After each lever flip the doorway must reach the other state
   within **{cap} game ticks** (20 ticks = 1 second), the whole build must come to rest (no block
   changing for {quiet} ticks, so no free-running clocks), and it must then stay unchanged for
   {hold} more ticks.
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

These were checked in the grader's own simulator.{physics_note}

- A piston's `facing` is the direction its head extends. Pistons push at most {push_limit} blocks.
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
- A repeater adds {repeater_unit} ticks per delay step, and stretches a pulse shorter than its delay to
  the length of its delay. A comparator adds 2. A torch switches 2 ticks after the block it
  is on changes.
{observer_fact}
- A piston that another piston pushes into a powered position (for example beside a
  redstone block) starts its own stroke the tick after it lands and has finished two ticks
  later.
- Observers do not fire merely for being placed. They fire when the cell they watch changes,
  which includes changes during settling.
{more_facts}
## Tools

{tools}
{starting}
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
- **Step** advances exactly the number of ticks you ask for (1 to {lab_step}) and lists every
  block change with its tick. Stepping 5 and then 3 is the same as stepping 8.
- **Rest** advances until no block has changed for {quiet} ticks in a row, which is the test's
  meaning of "at rest", or until a maximum you give (default 200). When it comes to rest the
  clock stands {quiet} ticks after the last change.
- **Look** and **view** report the current state and take no time.
- One lab world can run at most {lab_world} ticks in all. After that, start a new lab.
- The first item drop or falling block to appear is reported (`ENTITY appeared`); later ones are not.
- There is one lab world, and starting a new lab empties it. It is separate from the world
  `test`, `trace` and `view` use: they never disturb the lab and the lab never affects them.
- `trace` is the same thing done for you: with the hallway walls present, starting a lab with
  a complete design, then rest, flip, rest, flip, rest gives the same block changes on the
  same ticks as `trace` shows for two flips, counting from each flip.

{lab_tools}
## Budget

You have **{tests} test calls**, **{sims} trace/view calls** and **{lab} lab ticks**. Designs
rejected in step 1 are free. In the lab only ticks advanced by step and rest count; starting
a lab, flip, look and view are free.{minutes}
If you never submit, your smallest design that passed a test is used.

The first design that works is rarely the smallest. The budget is there to be used: once you
have a valid door, keep looking for a smaller one until you run out of calls or of ideas.

## Ground rules

{ground}
"""

# ---------------------------------------------------------------- kit 2
# Kit 1 is the frozen brief and tools of benchmark waves 1 to 6. Kit 2 adds the film (every
# tick of a run as data), structured test results, and facts that agents reported missing.
# Every fact below is asserted in tests/test_kit2.py. Kit 1 text is never touched.

MORE_FACTS = """
More facts, added after earlier runs reported them missing (all checked in the grader's simulator):

- Signal strength: dust next to a power source carries 15 and each further dust carries one
  less, so the 15th dust still powers a piston and the 16th carries nothing. A repeater
  restores it to 15.
- A block powered only by dust does not power other dust. Dust running into a stone does not
  switch on dust on the far side of that stone; a repeater running into the stone does.
- A sticky piston pulls back only the one block touching its head. If it pushed two blocks
  in a row, the far one stays where it was pushed.
- Dust sitting on a piston that faces north, south, east or west drops as an item the moment
  that piston extends, which fails the test. Dust on a down-facing piston stays.
- A lever can be attached to a piston. On the piston's back (for example standing on top of
  a down-facing piston) it stays put and powers that piston. On a side face (checked on top
  of an east-facing piston) it drops as an item when the piston starts to extend.
- A lever standing on the middle one of three down-facing pistons in a row switches all
  three: the middle one directly, the outer two through quasi-connectivity, and the lever's
  own update is enough for them to notice.
- A note block's `powered` state follows a powered block beside it, without passing power
  on. An observer watching the note block fires each time that state changes.
- An observer can watch another observer, so a line of observers all facing the same way
  carries a pulse; each one adds {observer_delay} ticks.
- An observer that a piston moves emits one pulse when it lands.
- Dust connects to a redstone block and to a target block beside it.
- Slime or honey in a frame cell (z = 0, beside the doorway) touches the hallway walls at
  z = 1 and z = -1. If a piston moves it, the wall block comes along, which fails the test.

Details of the rules that earlier runs asked about:

- The build region is exactly {rx0} <= x <= {rx1}, {ry0} <= y <= {ry1} and {rz0} <= z <= {rz1}.
- The lever's cell is never counted, wherever it is. It may sit outside the z = 0 layer
  (for example at z = 1 on a block that is at z = 0), as long as it is not in the hallway or its walls.
"""

FILM_ROW_CLI = ("| `./pd film design.json [--flips N] [--ticks T] [--out FILE]` | The same run as `trace`, saved as JSON:"
                " every tick of every flip. Uses one trace/view call |\n")

FILM_CLI = """### The film

`./pd film design.json` runs the design exactly as `trace` does, writes the whole run to
`design.film.json` and prints only the summary line for each flip. Use it when you want to
compute on a run instead of reading it: when exactly a piston fired, the state of every
block at some tick, or how two versions differ. The file holds:

```
{"task": {"width": W, "height": H, "track": "seamless"},
 "placement": {"at_rest": true, "last_change_tick": 0, "changes": [[t, x, y, z, before, after], ...]},
 "start": {"doorway": "###/###", "blocks": [[x, y, z, state], ...]},
 "flips": [{"flip": 1, "lever": "on", "at_rest": true, "last_change_tick": 9, "ticks_run": 29,
            "changes_total": 31, "complete": true,
            "ticks": [{"t": 0, "doorway": "###/###", "changes": [[x, y, z, before, after], ...]}, ...]}, ...],
 "entity": null, "protected_cell": null, "swept_box": {"min": [x, y, z], "max": [x, y, z]}}
```

- `start` is the build at rest before the first flip: every non-air block, hallway walls left out.
- `ticks` has one entry for every tick from `t = 0` to the last tick at which anything
  changed, including ticks where nothing did. `t = 0` is the instant of the flip, before any
  game tick: its changes are the ones the flip itself makes, such as dust power. Tick numbers
  match `trace`.
- `doorway` is the doorway at the end of that tick, as rows, top row first (`#` stone, `.` air,
  `m` moving, `?` other). Block states are written as in `trace`; an empty cell is `air`.
- `complete` is false only if one flip made more than 20,000 changes; the list is then cut short.
- `entity` and `protected_cell` say what appeared or which protected cell changed, with the
  tick counted from the start of the run; either one means the design is invalid.
- At most 8 flips. `--ticks` works as in `trace`.

"""

FILM_PY_ROWS = (
    "| `f = film(design, flips=2, ticks=None)` | The film as a `Film` object (one trace/view call). `f.data` is the JSON above;"
    " `f.save(path)`, `Film.load(path)`; `f.flips`; `f.ok` is true if every flip came to rest with no entity and no protected cell changed |\n"
    "| `f.doorway(flip)`, `f.doorway(flip, t)` | `[(t, rows), ...]` at each tick the doorway changed; or the rows at tick `t`. Flips count from 1 |\n"
    "| `f.changes(flip, grep=None)`, `f.first(flip, grep)` | `[(t, (x, y, z), before, after), ...]` in order; or the first one whose text contains `grep` (else `None`) |\n"
    "| `f.cell(x, y, z)` | `[(flip, t, state), ...]`: every state that cell took, starting with `(0, 0, state at rest)` |\n"
    "| `f.at(flip, t)`, `f.start()` | `{(x, y, z): state}` for every block after tick `t` of that flip (`flip=0`: before the first flip) |\n"
    "| `f.last_tick(flip)` | The last tick of that flip at which anything changed |\n"
)

TEST_PY_V1 = ("| `r = test(design)` | The full test. `r.valid`, `r.volume`, `r.dims`, `r.failures` (codes), `r.rejected`, `r.refused`, `r.text`;"
              " `print(r)` shows the report |\n")
TEST_PY_V2 = ("| `r = test(design)` | The full test. `r.valid`, `r.volume`, `r.dims`, `r.failures` (codes), `r.rejected`, `r.refused`, `r.text`;"
              " `print(r)` shows the report. Also `r.bbox`, `r.block_count`, `r.timings` (when valid: per flip, `to`, `reach_tick`, `reset_tick`)"
              " and `r.detail` (per failure: `code`, `message` and what the report shows for it, such as `doorway_at_end` or `timeline`) |\n")

PY_NOTES_V2 = """Two things about the Python session that earlier runs tripped over: it keeps imported
modules, so after editing a helper file of your own, reload it (`importlib.reload`) or run
`./pd py --reset`; and its output carries no time-left line, so use `print(status())` for that.

"""


def _kit2(tools, lab_tools, interface):
    """The kit 1 tool text with kit 2's additions. Fails loudly if kit 1's text has moved."""
    if interface != "cli":
        return tools, lab_tools   # the film is command-line only for now

    def put(text, anchor, new):
        if text.count(anchor) != 1:
            raise ValueError(f"kit 2: anchor not found exactly once: {anchor[:50]!r}")
        return text.replace(anchor, new + anchor)
    tools = put(tools, "| `./pd view design.json", FILM_ROW_CLI)
    tools = put(tools, "`pdbuild.py` is an optional Python helper", FILM_CLI)
    if lab_tools.count(TEST_PY_V1) != 1:
        raise ValueError("kit 2: the test row of the Python table has moved")
    lab_tools = lab_tools.replace(TEST_PY_V1, TEST_PY_V2)
    lab_tools = put(lab_tools, "| `submit(design)`, `status()`, `blocks()` |", FILM_PY_ROWS)
    lab_tools = put(lab_tools, "`example_lab.py` is a short worked example", PY_NOTES_V2)
    return tools, lab_tools


TOOLS = {
    "cli": """Run these from this folder.

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
""",
    "tools": """| Tool | What it does |
|---|---|
| `pd_status()` | Task, remaining budget, best result so far |
| `pd_blocks()` | Allowed blocks and their properties |
| `pd_test(design)` | The full test: valid or not, why not, volume, timings |
| `pd_trace(design, flips, ticks, grep)` | Every block change, tick by tick, after placement and after each flip |
| `pd_view(design, flips, z)` | ASCII picture of the build, one grid per z layer |
| `pd_submit(design)` | Nominate your final design. You can submit again; the last one counts |

`design` is the design JSON as text{sandbox_note}.
""",
}

LAB_TOOLS = {
    "cli": """| Command | What it does |
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
""",
    "tools": """| Tool | What it does |
|---|---|
| `pd_lab_new(blocks, walls)` | Empty the lab and place these blocks: a design, or a bare JSON list of blocks, as text |
| `pd_lab_flip(x, y, z)` | Flip the lever at that position |
| `pd_lab_step(ticks, grep)` | Advance exactly `ticks` ticks |
| `pd_lab_rest(max_ticks, grep)` | Advance until at rest |
| `pd_lab_look(cells, grep)` | State of every block (hallway walls left out), or of the cells named (an empty cell reads `air`), and the doorway |
| `pd_lab_view(z)` | ASCII picture of the lab now; it always includes the doorway cells |
""",
}

MINUTES = (" You also have **{minutes} minutes**, counted from your\nfirst tool call. This is wall-clock time: thinking between calls counts too. Every"
           " tool reply ends with the time left. Once the time is up, `test`, `trace`, `view` and the lab are refused;"
           " status, the block list and submit still work.")

GROUND = {
    "cli": """- Work only inside this folder. Do not read or change anything outside it, and do not use the internet.
- The grader's verdict is final. Do not try to interfere with it.
- Before you finish, run `./pd submit` on the design you want scored.""",
    "tools": """- The grader's verdict is final. Do not try to interfere with it.
- Before you finish, call `pd_submit` with the design you want scored.""",
}

STARTING = {
    "cli": """
`start.json` is a working design for this task. It is valid but large (volume {volume}). You
can study it, improve it, or ignore it and start over.
""",
    "tools": """
Here is a working design for this task. It is valid but large (volume {volume}). You can
study it, improve it, or ignore it and start over.

```json
{design}
```
""",
}


def compact(design):
    """Design JSON with one block per line, which is far easier to read than indent-based output."""
    lines = [json.dumps(b) for b in design["blocks"]]
    return '{"initial_state": ' + json.dumps(design["initial_state"]) + ',\n "blocks": [\n  ' + ",\n  ".join(lines) + "\n ]}\n"


def physics_facts(physics=None):
    """Brief text that depends on the physics settings. Vanilla settings give the original
    wording exactly. Only settings whose behaviour was measured in the grader are accepted."""
    from .kernel import PHYSICS_DEFAULTS, physics_key
    changed = physics_key(physics)
    v = {**PHYSICS_DEFAULTS, **changed}
    d, pulse = v["observer_delay"], v["observer_pulse"]
    if pulse == 2:
        sticky = (f"A sticky\n  piston given that 2-tick pulse pushes its block and leaves it behind; the next pulse\n"
                  f"  fetches it back.")
    elif pulse >= 4:
        sticky = (f"A sticky\n  piston given that {pulse}-tick pulse finishes its push and then pulls its block back;\n"
                  f"  it does not leave the block behind.")
    else:
        raise ValueError(f"observer_pulse={pulse}: sticky-piston behaviour not measured")
    observer = f"- An observer turns on {d} ticks after the change it sees and off {pulse} ticks later. {sticky}"
    note = ""
    if changed:
        names = {"repeater_unit": ("a repeater delay step", "ticks"), "push_limit": ("the most blocks a piston can push", "blocks"),
                 "observer_delay": ("an observer's reaction time", "ticks"), "observer_pulse": ("an observer's pulse length", "ticks")}
        parts = [f"{names[k][0]} is {val} {names[k][1]} (standard: {PHYSICS_DEFAULTS[k]})" for k, val in changed.items()]
        note = ("\n\n**This world's physics are changed.** It is Minecraft Java " + rules.GAME_VERSION + " except that "
                + "; ".join(parts) + ". Everything else is standard. The facts below already describe this world, "
                "and designs that work in standard Minecraft may not work here.")
    return {"physics_note": note, "push_limit": v["push_limit"], "repeater_unit": v["repeater_unit"], "observer_fact": observer}, d


def brief(n, track, budget, interface="cli", starting=None, starting_volume=None, sandbox=False, minutes=None, physics=None, kit=1):
    w, h = rules.dims(n)
    tools_text, lab_text, more = TOOLS[interface], LAB_TOOLS[interface], ""
    if kit >= 2:
        tools_text, lab_text = _kit2(tools_text, lab_text, interface)
        lo, hi = rules.region(n)
        more = MORE_FACTS.format(observer_delay=physics_facts(physics)[1], rx0=lo[0], rx1=hi[0], ry0=lo[1], ry1=hi[1],
                                 rz0=lo[2], rz1=hi[2])
    start_text = ""
    if starting:
        start_text = STARTING[interface].format(volume=starting_volume, design=compact(starting).rstrip())
    note = ", or the path of a JSON file you wrote in your sandbox" if sandbox else ""
    return BRIEF.format(
        w=w, h=h, mw=w - 1, mh=h - 1, h1=h + 1, cells=w * h, version=rules.GAME_VERSION,
        shape_note="" if w == h else SHAPE_NOTE.format(w=w, h=h),
        track_rule=TRACK_RULE[track].format(ring=2 * (w + h)), example=compact(EXAMPLE).rstrip(),
        settle=rules.SETTLE_CAP, cap=rules.TIME_CAP, quiet=rules.QUIET, hold=rules.HOLD,
        tools=tools_text.replace("{sandbox_note}", note), starting=start_text, ground=GROUND[interface], more_facts=more,
        tests=budget["test"], sims=budget["sim"], lab=budget.get("lab", DEFAULT_BUDGET["lab"]),
        lab_step=LAB_MAX_STEP, lab_world=LAB_WORLD_TICKS, lab_tools=lab_text,
        minutes=MINUTES.format(minutes=minutes) if minutes else "",
        **physics_facts(physics)[0],
    )


def make_kit(out_dir, n, track, server_url, budget, starting=None, starting_volume=None, minutes=None, physics=None, kit=1):
    """Write a working folder for a command-line agent. kit=2 overlays the files in kit_template_v2/."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("pd", "pdbuild.py", "pdlab.py", "example_lab.py"):
        shutil.copy(TEMPLATE / name, out / name)
    if kit >= 2:
        for f in sorted((TEMPLATE.parent / "kit_template_v2").iterdir()):
            shutil.copy(f, out / f.name)
    (out / "pd").chmod(0o755)
    (out / ".pd_server").write_text(server_url + "\n")
    (out / "example_1x1.json").write_text(compact(EXAMPLE))
    design = json.loads(Path(starting).read_text()) if starting else None
    if design:
        (out / "start.json").write_text(compact(design))
    (out / "TASK.md").write_text(brief(n, track, budget, "cli", design, starting_volume, minutes=minutes, physics=physics, kit=kit))
    return out
