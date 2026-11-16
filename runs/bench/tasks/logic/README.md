# Timing and sequential-logic tasks (repair / port / hidden_rule)

Each task gives the agent a small redstone circuit that is broken or mis-tuned and a behaviour spec.
The agent has to change the build until the output trace matches the spec. The grader is the
unmodified Minecraft Java 26.3 kernel (`grader/kernel`), run headless one tick at a time.

## Folder

| path | what |
|---|---|
| `lib.py` | harness, kernel jobs, per-tick trace reconstruction, spec comparison |
| `check.py` | CLI checker: `python3 check.py tasks/<id>.json [build.json \| --start \| --reference] [--physics '{...}']` |
| `circuits.py` | the reference circuits (block lists and input schedules) |
| `refs/<circuit>.json` | each reference build with its trace as measured in vanilla 26.3 |
| `edits.py` | fault model (how builds were broken) and the single-edit neighbourhood used for hardness proofs |
| `make_tasks.py` | `refs`, `repair`, `port`, `verify` stages that produce and re-check `tasks/` |
| `tasks/<id>.json` | the tasks |
| `work/cache.json` | cached sweep summaries (safe to delete) |
| `probe.py` | prints every circuit's trace under a given physics (development aid) |

## Harness

Every circuit uses the same harness. Its cells belong to the checker: the checker places them, and
the build may not occupy, move or replace them. A moved harness block fails the build with
`harness_changed`.

- **Input A:** a wall lever at `(-1, 1, 0)`, `facing=west`, attached to a stone block at `(0, 1, 0)`.
  The lever starts off.
- **Output Q:** a `note_block` at a per-task position. Q is **on** while the note block's `powered`
  property is true. The note block is on the allow-list, updates in the same tick as its input
  (a redstone lamp would add a 4 gt off-delay), and conducts. Strongly powering Q can therefore
  feed back into dust next to it; the `extender` reference avoids this deliberately.

`lib.output_on` also understands other output kinds (`redstone_lamp` `lit`, piston `extended`,
observer/repeater `powered`, target/wire `power > 0`). The kernel places any block state it can
parse, including off-list blocks such as `redstone_lamp`. All tasks here use note blocks.

## Spec format (`task["spec"]`)

```json
{
  "inputs":  [{"t": 10, "lever": "A"}, {"t": 47, "lever": "A"}, ...],
  "end":     235,
  "tol":     0,
  "latency": [0, 0],
  "outputs": {"Q": {"initial": false, "edges": [[26, true], [63, false], ...]}}
}
```

- **Time:** t = 0 is the end of settling. After placement the build gets up to 80 ticks and must
  then stay unchanged for 20 ticks, or it fails with `not_settled`.
- **Inputs:** each entry flips that lever after tick `t` has run. The run ends at tick `end`.
- **Sampling:** Q is sampled once per tick, after every event at that tick. A change that reverts
  within the same tick is invisible.
- **Edges:** the edge `[t, v]` means Q is `v` at tick `t` and was not `v` at `t - 1`.
- **Pass rule:**
  - Q's initial value equals `initial`.
  - Q has exactly as many edges as listed.
  - The values match edge for edge.
  - Some shift `s` in `latency` exists with `|t_got - (t_want + s)| <= tol` for every edge.
- **Strictness:** every shipped task uses `tol = 0` and `latency = [0, 0]`, so the trace must match
  tick for tick. `latency` allows a uniform phase offset (for clock-like specs); `tol` allows
  per-edge jitter.

**Anti-hard-wiring.** Every schedule has at least 3 full off→on→off cycles; the T flip-flop has 4.
The gaps are irregular (for example 37, 41, 29, 45, 33 ticks), so a free-running clock cannot
phase-lock onto them. Each spec has at least 4 edges in both directions. Two shortcuts both fail:
- A redstone block driving Q fails `wrong_initial` (or `wrong_edge_count`).
- Wiring Q straight to the lever fails `wrong_timing` on every task. The pulse, T flip-flop and
  clock tasks also fail it on edge count.

## Limits (`task["limits"]`)

- **Box:** `bbox` = the reference build plus the harness (plus the reference fix for port tasks),
  padded by 1 cell on x and z and 1 cell upward, with the bottom at y = 0. Blocks placed outside
  fail with `outside_bbox`. A block that appears outside the box during the run (for example
  pushed by a piston) fails with `left_bbox`.
- **Budget:** `max_blocks` = the reference block count (the larger of start and fix for ports)
  + 4. Support blocks count.

"Rebuild bigger from scratch" is therefore not available. Rebuilding inside the box is allowed if
it fits.

## Other checks

- Allow-list and property rules: `pdgrader.validate.validate_part`.
- No entities (item drops and falling blocks) at any point.
- The levers must still be present.

## Task kinds

Every task file carries:

- `start.blocks`: what the agent receives
- `reference.blocks`: a known passing build
- `physics` and `physics_disclosed`
- `provenance`: the faults applied, or the reference-fix edits
- `hardness`
- `verified`: a recorded fresh check, with the start build failing and the reference passing

The task kinds:

- **repair** (vanilla physics): the reference with 1–3 faults from `edits.faults`. The faults are
  mis-set repeater delays, reversed or swapped repeaters/comparators, flipped comparator modes,
  turned observers, swapped pistons, missing dust or torches, and stray stone or redstone blocks
  next to the circuit.
  - `easy`: one fault; undoing it fixes the build.
  - `medium`: several faults, but one edit restores the spec.
  - `hard`: no single edit in the **single-edit neighbourhood** restores the spec. That
    neighbourhood is every non-harness cell of the task box set to every one of 57 states:
    air, plain/special blocks, pistons, sticky pistons and observers in 6 facings, repeaters in
    4 facings × 4 delays, comparators in 4 facings × 2 modes, wire, torch, and wall torches.
    This was checked exhaustively in the kernel.
- **port**: the spec is the vanilla trace, fixed in game ticks. The physics changes (for example
  `repeater_unit = 3`) and the brief says how. The vanilla build was confirmed to miss the spec
  under the new physics, and a hand-made reference fix was confirmed to pass. The difficulty
  comes from the same neighbourhood sweep under the new physics:
  - `easy`: some single edit fixes it.
  - `hard`: none does.
- **hidden_rule**: like port, but the brief only says that one undisclosed physics rule differs.

## Re-running

```
python3 make_tasks.py refs     # ~1 min
python3 make_tasks.py repair   # sweeps; tens of minutes
python3 make_tasks.py port
python3 make_tasks.py verify   # fresh start-fails / reference-passes check of every task
```

The scripts run one kernel at a time (heap 1G, booted again only when the physics changes), with
scratch space in `/private/tmp/claude-501/tasks_logic_k`. They refuse to boot when less than
300 MB is free and wait up to 10 minutes for space. A single check takes about 0.05 s once the
kernel is up; booting takes about 15–20 s. Batching several builds into one kernel job is
implemented (`run_cases(batch=...)`) but was slower, so it is off.

## What the checker cannot catch

- **Only Q is observed.** Internal behaviour is not judged, for example a build that keeps
  oscillating internally while Q is correct.
- **Behaviour outside the schedule.** The spec samples one fixed input schedule. A build tuned to
  exactly these toggle times could pass. Examples are counting toggles, or behaving differently for
  gaps shorter than the shortest gap in the schedule (23 ticks) or for pulses shorter than about
  20 ticks. Specs do not test fast lever toggling.
- **Placement position.** Each build is checked at one world position (origin `(0, 100, 0)`) and
  one orientation. Translation and rotation robustness are not checked.
- **Sub-tick glitches** are invisible, because Q is sampled once per tick.
- **Neighbourhood limits.** Hardness is relative to the 57-state single-edit neighbourhood inside
  the box. Block states outside the palette (for example other note-block notes or glazed
  terracotta) were not swept.
- **One fix per task.** Port and hidden-rule fixes are one possible solution each. Other valid
  solutions exist, and the checker accepts any of them.

## Task set (31 tasks, all verified)

| task | kind | difficulty | physics | budget | single-edit neighbours (passing) |
|---|---|---|---|---|---|
| `logic_hidden_rule_delay12_repeaterunit1` | hidden_rule | hard | {"repeater_unit": 1} | 10 | 3864 (0) |
| `logic_hidden_rule_extender_repeaterunit1` | hidden_rule | hard | {"repeater_unit": 1} | 22 | 6552 (0) |
| `logic_hidden_rule_obs_chain_observerpulse1` | hidden_rule | hard | {"observer_pulse": 1} | 10 | 4368 (0) |
| `logic_hidden_rule_tff_observerdelay1` | hidden_rule | easy | {"observer_delay": 1} | 30 | 9912 (6) |
| `logic_port_clock20_repeaterunit1` | port | easy | {"repeater_unit": 1} | 17 | 7392 (1) |
| `logic_port_clock20_repeaterunit3` | port | hard | {"repeater_unit": 3} | 17 | 7392 (0) |
| `logic_port_delay12_repeaterunit3` | port | easy | {"repeater_unit": 3} | 10 | 3864 (7) |
| `logic_port_delay16_repeaterunit1` | port | hard | {"repeater_unit": 1} | 16 | 5376 (0) |
| `logic_port_delay16_repeaterunit3` | port | hard | {"repeater_unit": 3} | 16 | 5376 (0) |
| `logic_port_extender_repeaterunit3` | port | easy | {"repeater_unit": 3} | 22 | 6552 (7) |
| `logic_port_obs_chain_observerdelay1` | port | hard | {"observer_delay": 1} | 10 | 4368 (0) |
| `logic_port_obs_chain_observerdelay3` | port | easy | {"observer_delay": 3} | 9 | 4368 (15) |
| `logic_port_rise_mono_repeaterunit1` | port | easy | {"repeater_unit": 1} | 16 | 5208 (1) |
| `logic_port_tff_observerdelay3` | port | easy | {"observer_delay": 3} | 30 | 9912 (1) |
| `logic_repair_clock20_easy` | repair | easy | vanilla | 17 |   |
| `logic_repair_clock20_hard` | repair | hard | vanilla | 17 | 7392 (0) |
| `logic_repair_delay12_easy` | repair | easy | vanilla | 10 |   |
| `logic_repair_delay12_medium` | repair | medium | vanilla | 10 | 3864 (3) |
| `logic_repair_delay16_easy` | repair | easy | vanilla | 16 |   |
| `logic_repair_delay16_hard` | repair | hard | vanilla | 16 | 5376 (0) |
| `logic_repair_delay16_medium` | repair | medium | vanilla | 16 |   |
| `logic_repair_extender_easy` | repair | easy | vanilla | 22 |   |
| `logic_repair_extender_hard` | repair | hard | vanilla | 22 | 6552 (0) |
| `logic_repair_fall_mono_easy` | repair | easy | vanilla | 16 |   |
| `logic_repair_fall_mono_hard` | repair | hard | vanilla | 16 | 5208 (0) |
| `logic_repair_obs_chain_easy` | repair | easy | vanilla | 9 |   |
| `logic_repair_obs_chain_hard` | repair | hard | vanilla | 9 | 4368 (0) |
| `logic_repair_rise_mono_easy` | repair | easy | vanilla | 16 |   |
| `logic_repair_rise_mono_hard` | repair | hard | vanilla | 16 | 5208 (0) |
| `logic_repair_tff_easy` | repair | easy | vanilla | 30 |   |
| `logic_repair_tff_hard` | repair | hard | vanilla | 30 | 9912 (0) |

## Reference circuits (vanilla traces in `refs/`)

| circuit | blocks | behaviour |
|---|---|---|
| `clock20` | 13 | While the lever is on, Q blinks 10 gt on / 10 gt off; while it is off, Q stays off. |
| `delay12` | 6 | Q follows the lever 12 game ticks later on both edges (repeaters 4+2 = 8+4 gt). |
| `delay16` | 12 | Q follows the lever 16 game ticks later on both edges (repeaters 3+3+2 = 6+6+4 gt). |
| `extender` | 18 | Q turns on with the lever and turns off 12 game ticks after it (slow path 8+4 gt). |
| `fall_mono` | 12 | On each lever-off, Q gives one short pulse; lever-on does nothing. |
| `obs_chain` | 5 | Each lever flip (either way) makes one short Q pulse after three observer delays. |
| `rise_mono` | 12 | On each lever-on, Q gives one short pulse (comparator 2 gt, side repeater 4 gt); lever-off does nothing. |
| `tff` | 26 | Each lever-on toggles Q; lever-off does nothing. |

Only delay12 and delay16 have a `medium` repair. The search draws up to 40 random 2–3-fault breaks and runs at most 3 full sweeps per circuit. Once the hard task was found, no further sweeps were run, and none of the remaining draws could be fixed by undoing a single fault. delay12 got no `hard` task: in each of its 3 sweeps, one compensating single edit always existed. `make_tasks.py verify` also checks a hard-wire cheat on every task: the reference plus a redstone block beside Q must fail.
