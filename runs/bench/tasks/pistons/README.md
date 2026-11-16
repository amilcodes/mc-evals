# Piston machines: repair and physics-adaptation tasks

Task family **pistons** for Piston Door Bench: piston machines other than doors. The agent gets a
build that is broken (repair) or that fails under changed physics (port, hidden_rule) and must make
it meet a behavioural spec, checked tick by tick in the real 26.3 engine (`grader/` kernel).

## Files

| path | what |
|---|---|
| `check.py` | spec checker; `check(kernel, spec, build)`; CLI `python3 check.py tasks/<id>.json [build.json \| --start]` |
| `machines.py` | the reference machines and their specs (source of truth) |
| `refs/<name>.json` | each reference build + spec, verified under vanilla physics |
| `tasks/<id>.json` | one task each (prompt, spec, physics, start build, reference solution, verification record) |
| `index.json` | task list: id, kind, difficulty, machine, physics |
| `build_tasks.py` | repair-task generation: natural-break scans, single-edit neighbourhood search, task writer |
| `gen_ports.py` | port / hidden_rule generation (one kernel per physics) |
| `verify_all.py`, `verify_all.json` | re-checks every task (start fails, reference passes) under its physics; refreshes refs, runs selftest |
| `selftest.py`, `selftest_result.json` | hacks the checker must reject, and the result of the last run |
| `work/` | raw scan outputs (natural-break scans, physics scans) |

Kernels must be started through `check.kernel_for(physics)`, which keeps scratch worlds out of
`grader/` (under `/private/tmp/claude-501/tasks_pistons_k`). One kernel per physics setting: the
physics is fixed when the JVM starts.

## Build format

A build is a list of blocks, the same format as door submissions:
`[{"pos": [x, y, z], "id": "minecraft:sticky_piston", "props": {"facing": "east"}}, ...]`
(or `{"blocks": [...]}`). Coordinates are local; the grader places local (0,0,0) at world (0,100,0).
x is east, y up, z south. Facings are the game's block states: piston = direction the head pushes,
repeater = side the input comes from, observer = side its face watches. Only allow-listed blocks and
properties (`grader/pdgrader/rules.py`) are accepted; an extended piston needs its head (and vice versa).
The lever is part of the build and must sit exactly at `spec.lever`.

## Spec format

```jsonc
{
  "lever": [x, y, z],                     // the one lever; starts off
  "box": {"min": [..], "max": [..]},      // every block, at every tick, must stay inside
  "block_budget": 33,                     // max blocks in the build, lever included
  "states": {                              // required block ids at rest
    "off": [{"at": [2, 0, 0], "is": "lime_concrete"}, {"at": [[3, 4], 0, 0], "is": "air"}],
    "on":  [{"at": [4, 0, 0], "is": "lime_concrete"}, {"at": [2, 0, 0], "is": ["sticky_piston", "piston"]}]
  },
  "schedule": [0, 3, 7, 1, 11, 2],        // idle ticks before each lever flip; >= 4 flips
  "time_cap": 60,                          // ticks per flip to come to rest (default 60)
  "reach_cap": null,                       // optional: ticks per flip for the target cells to be reached for good
  "hold": 40, "quiet": 20, "settle_cap": 40,
  "keep_clear": [[x, y, z], [[x0, x1], y, z]],   // cells that must be empty at every tick (frozen air)
  "fixed": [[x, y, z, "minecraft:smooth_stone"]], // cells that must hold that block at every tick
  "conserve": {"minecraft:lime_concrete": 1},     // exact count in the build and at every rest
  "periodic": true,                        // whole build at rest == its state two flips earlier
  "forbid_entities": true                  // item drops / falling blocks fail
}
```

`at` coordinates are an int or an inclusive `[lo, hi]` range; `is` is a block id (namespace optional),
`"air"`, or a list of acceptable ids. Properties are not compared, only block ids.

### What the checker does

1. **Static**: allow-list and piston-head consistency (`validate_part`), one lever at `spec.lever`,
   all blocks in `box`, count <= `block_budget`, `fixed` cells present, `keep_clear` cells empty,
   `conserve` counts exact.
2. **Simulation** (one kernel job): clear, place (schematic paste semantics: observers do not fire on
   placement), run until quiet (`quiet` ticks without change, within `settle_cap`), snapshot; then for
   each flip: idle `schedule[i]` ticks (nothing may change), flip the lever, run until quiet (must be
   within `time_cap`), run `hold` more ticks (nothing may change), snapshot.
3. **Per flip**: target cells of the required state (`on` after odd flips, `off` after even flips and
   at the start), `conserve` counts at rest, periodicity (full snapshot equals the one two flips before),
   optional `reach_cap` (reconstructed from the per-tick change log).
4. **Whole run**: no entity ever (item drop, falling block), no `keep_clear`/`fixed` cell ever changed,
   no block ever outside the box (`escaped`).

Result: `{"pass", "stage", "failures": [{"code", "message", ...}], "toggles_passed", "timings",
"block_count"}`. Codes: `lever`, `outside_box`, `over_budget`, `fixed_cell`, `keep_clear`, `conserve`,
`not_settled`, `wrong_start`, `not_at_rest`, `lever_missing`, `wrong_state`, `too_slow`,
`did_not_hold`, `not_periodic`, `entity`, `frozen_cell`, `left_box`, plus the allow-list codes.

### Anti-gaming

- Both rest states are checked after **every** flip (6 flips by default), so a build that only ever
  extends, or only works once, fails (`wrong_state` / `not_periodic`).
- `conserve` + `keep_clear` stop "bring a second payload in from another side" and parking spare
  copies; for the extenders the cells around the track are keep-clear, so the payload can only reach the
  target cell along the track.
- `periodic` stops machines that drift, leak blocks or leave pistons in a different state each cycle.
- Uneven idle gaps (`schedule`) shift the flip phase relative to any clock.
- `block_budget` (start or reference size + 2) and the tight `box` (reference bounding box + 1) mean
  a from-scratch rebuild is not a free answer.

### What it cannot catch

- Behaviour under flips faster than `time_cap + hold` apart (mid-motion flips), other placements or
  rotations (no translation test here), or other chunk alignments.
- Cells not named in `states`, `fixed`, `keep_clear` may do anything as long as the whole build is
  periodic and stays in the box (e.g. extra pistons idling inside the box).
- Block properties are not compared in targets (a payload slot accepts any facing/state of that id).
- `reach_cap` relies on the change log; if a flip produces more than 6000 changes the reach tick is unknown
  (fails only if `reach_cap` is set). No task currently sets `reach_cap`.
- Only one lever input; no partial credit beyond `toggles_passed`.

## Machines (vanilla 26.3, verified)

| name | what | blocks | rest ticks on / off |
|---|---|---|---|
| `dpe` | double piston extender: two sticky pistons; front piston fires from a power block it lands on; retraction by an observer-pulse "grab" | 31 | 26 / 28 |
| `tpe` | triple piston extender: three sticky pistons, five under-track power blocks, level signals from the south, observer pulses and a slow hold from the north | 149 | 50 / 52 |
| `swapper` | block swapper: slot shows red (lever off) or blue (on); sticky side piston held out by a torch; OR-of-two-delays makes the torch go out fast and relight late, so the pistons never collide | 31 | 12 / 16 |
| `hatch` | 2x2 flush floor hatch: slime pad pulled down by one sticky piston (8 blocks moved); power through obsidian so the pad cannot drag it | 26 | 4 / 4 |
| `row_slide` | 6 concrete on 6 slime slid sideways by one sticky piston: exactly 12 blocks, the vanilla push limit | 15 | 3 / 3 |
| `row_push` | 10-block row shuttled along its own axis by two normal pistons facing each other, sequenced so they never fight | 60 | 12 / 16 |
| `elevator` | 3-slime platform with 3 concrete lifted 1 cell; glazed-terracotta posts beside it are fixed (they do not stick to slime) | 21 | 3 / 3 |

## Tasks

Kinds:
- **repair**: the reference with 1-3 edits (an edit sets one cell to one block state, or air).
  `easy` = one edit (the inverse edit fixes it). Multi-edit tasks were checked against the full
  single-edit neighbourhood: every cell of the box (except lever, `fixed`, `keep_clear`) times the
  palette in `build_tasks.generic_palette()` plus every exact block state used by the start or reference
  build. `hard` = no single edit passes; `medium` = some single edit passes (listed in the task).
- **port**: works under vanilla, fails under the stated physics (`task.physics`, disclosed in the prompt).
  `reference_solution` is a verified fix under that physics.
- **hidden_rule**: as port, but the prompt does not say which mechanic changed (`disclose_physics: false`).
  The grader still runs with `task.physics`.

Difficulty for port / hidden_rule is by the size of the reference fix (cells that differ from the start):
1 = easy, 2-4 = medium, more = hard. Those starts are either the vanilla reference (push-limit ports and
the slow-repeater TPE, whose fixes are new designs in `machines.PORT_FIXES`) or a one-edit variant of the
reference that passes in vanilla but fails under the physics, found by checking all 397 vanilla-passing
natural edits under each setting (`work/variants_*.json`). No single-edit search was run on ports.

### Task list (34, all verified)

| kind | count | tasks |
|---|---|---|
| repair easy (1 edit) | 16 | dpe e1-e3, tpe e1-e2, swapper e1-e3, hatch e1-e2, row_slide e1-e2, row_push e1-e2, elevator e1-e2 |
| repair hard (2-3 edits, 0 single-edit fixes) | 6 | dpe_h1 (2 edits), dpe_h2 (3), swapper_h1, hatch_h1, row_slide_h1, elevator_h1 (2 each); 10.6k-20.7k edits searched per task |
| port | 8 | row_slide@push_limit 11 (hard), hatch@push_limit 7 (medium), tpe@repeater_unit 4 (hard, re-derived schedule), dpe / swapper / row_push @repeater_unit 1, swapper@repeater_unit 3, tpe@observer_delay 1 (easy) |
| hidden_rule | 4 | row_slide@push_limit 9 (hard), hatch@push_limit 5 (medium), dpe@repeater_unit 1, tpe@observer_delay 1 (easy) |

Physics sensitivity of the references (`work/physics_*.json`): push_limit breaks row_slide (<12),
row_push (<10), hatch (<8), elevator (<6); repeater_unit 4 breaks only the TPE (too slow for its cap);
repeater_unit 1/3, observer_delay 1/4 and observer_pulse 1/4 break none of the references (they have
2+ tick margins), which is why the timing ports start from tuned one-edit variants. observer_pulse broke
no variant either, so there is no observer_pulse task. row_push and elevator have no push-limit port:
a contiguous 10-block row cannot be moved under a smaller limit, and the elevator spec requires a slime
platform, which always sticks together.

Every task records `verification.start` (must fail) and `verification.reference` (must pass), both
under the task's physics, and `verified: true`.

## Re-verifying

```
python3 check.py tasks/<id>.json            # reference solution, under the task's physics
python3 check.py tasks/<id>.json --start    # the starting build (expected to fail)
python3 selftest.py                         # hacks must fail, references pass (vanilla)
```
