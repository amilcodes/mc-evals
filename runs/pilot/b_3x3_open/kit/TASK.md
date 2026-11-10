# Task: the smallest working 3x3 piston door

Design a redstone piston door for Minecraft Java Edition 26.3 (unmodified game rules) and make
it as small as you can. A grader builds your design in the real game engine, operates it,
and measures it. You have tools to test designs and to watch what they do tick by tick.

Your score is based on the **volume of the bounding box** of your final design, provided it
passes every rule below. A design that breaks a rule scores zero, so a working door comes
first and a smaller one second.

## The world

Coordinates are relative to the doorway. +x is east, +y is up, +z is south (north is -z).

- **Doorway:** the 3x3 cells `(x, y, 0)` with `0 <= x <= 2` and `0 <= y <= 2`.
- **Hallway:** the same 3x3 column at every other z. It runs straight through the doorway
  in both directions and must stay empty at all times.
- **Hallway walls:** every cell beside the hallway (left, right, above, below) at `z != 0`
  is filled with stone by the grader before your design is placed. These blocks are not
  yours: you may not place anything there, and nothing may move or replace them. They do not
  count toward your size. They are ordinary stone, so they conduct redstone power and can
  support dust placed on top of them.
- **Everything else is empty air**, including the z = 0 layer around the doorway. Blocks do
  not need support unless the block itself requires it (dust, torches and levers do).
- You may build anywhere within 24 blocks of the doorway.

The door is **closed** when all 9 doorway cells hold `stone`, and **open** when all 9 are air.

**Track: open.** There is no rule about what can be seen. Any door that works counts.

## What you submit

A JSON file:

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
  doorway cells must contain `stone` in your block list.
- Exactly one `lever`, switched off. It is the only input. Each flip of the lever must
  toggle the door. Which lever position means open is up to you.
- Only blocks from the allow-list (`./pd blocks`). Properties you leave out take the game's
  defaults. Leave out redstone dust's shape and power; the game works them out.
- If a piston starts extended you must also list its `piston_head` in the cell in front of it.

## How a design is tested

1. **Checked** against the format and placement rules. Problems are reported with positions
   and this does not use up a test.
2. **Placed and settled.** All blocks appear at once, then every block receives one update.
   The build must stop changing within 40 ticks and the doorway must match `initial_state`.
   A block that cannot exist where you put it (dust with nothing under it) disappears, and
   you get a warning.
3. **Cycled** several times. After each lever flip the doorway must reach the other state
   within **200 game ticks** (20 ticks = 1 second), the whole build must come to rest (no block
   changing for 20 ticks, so no free-running clocks), and it must then stay unchanged for
   40 more ticks.
4. **Throughout:** no entities may appear (a dropped item counts, for example dust whose
   support was pulled away), the hallway must stay empty, and the hallway walls must not change.

Your final design gets one stricter test with more cycles and flips at varied moments
after the build has come to rest. Flips never arrive while it is still moving.

## Size

Volume = width x height x depth of the smallest box containing every cell one of your
blocks occupied at any moment (including blocks in motion and extended piston heads),
plus the doorway itself. The lever is not counted. The grader's hallway walls are not counted.

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
- Redstone dust needs a solid block under it. Dust powers the block it sits on and the
  block or component it points at.
- Java Edition mechanics apply, including quasi-connectivity and short-pulse piston behaviour.

## Tools

Run these from this folder.

| Command | What it does |
|---|---|
| `./pd status` | Task, remaining budget, best result so far |
| `./pd blocks` | Allowed blocks and their properties |
| `./pd test design.json` | The full test: valid or not, why not, volume, timings |
| `./pd trace design.json [--flips N] [--ticks T] [--grep TEXT]` | Every block change, tick by tick, after placement and after each flip |
| `./pd view design.json [--flips N] [--z A..B]` | ASCII picture of the build, one grid per z layer |
| `./pd submit design.json` | Nominate your final design. You can submit again; the last one counts |

`pdbuild.py` is an optional Python helper for writing designs (`from pdbuild import Design`).
`example_1x1.json` is the one-cell example above; try `./pd trace example_1x1.json` to see the output format.

## Budget

You have **120 test calls** and **300 trace/view calls**. Designs rejected in step 1 are free.
If you never submit, your smallest design that passed `test` is used.

## Ground rules

- Work only inside this folder. Do not read or change anything outside it, and do not use the internet.
- The grader's verdict is final. Do not try to interfere with it.
- Before you finish, run `./pd submit` on the design you want scored.
