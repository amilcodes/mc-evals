# Internal grounding: the Piston Door Bench simulator, its doors and its run data

All source links are relative to the project root
`/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/`.
"Measured" means I ran the existing grader read-only on 2026-11-16 (Apple M4, 10 cores, 16 GB). The scripts and raw output are in `runs/bench/search_pilot/` (`timeit.py`, `verify.py`, `timing.json`, `blocks.py`, `claim_b.py`, `space.py`). Simulator scratch worlds were redirected to that folder, and no project file was changed. Volume is the bounding-box volume in blocks (lower is better). Ticks are game ticks (20 per second).

## 1. Simulator capability: what the kernel exposes, the agents' feedback, and how changed physics works

### Takeaway
The kernel is unmodified Minecraft 26.3 (Mojang's headless GameTestServer) driven one `ServerLevel.tick` at a time through a JSON job protocol. It can place any block-state layout in a 48×48×48 region, step exact tick counts, and continue a world between jobs. For every tick it reports each changed cell (old state to new state), the doorway pattern, the count of moving pistons, entities, and protected-cell violations. Agents see this as text traces, plus a structured "film" in kit 2. Changed physics comes from a Java agent that rewrites integer constants in Minecraft's bytecode as classes load.

### Cited Findings
- **Architecture.** `PdKernel.java` starts Mojang's own headless test server and holds it open with a never-finishing test (`pd:hold`). It then takes over the server thread, so every tick is an explicit `level.tick(...)` call. The source says "Nothing in the game is patched." — [grader/kernel/src/pd/PdKernel.java L52-63, L118-130](<grader/kernel/src/pd/PdKernel.java>); [grader/pdgrader/kernel.py L114-143](<grader/pdgrader/kernel.py>)
- **Protocol.** stdin takes one JSON job path per line, and the result goes to `<job>.result.json` followed by `PDK_DONE`. A job has `origin`, `region`, door size, `door_block`, `ignore` and `frozen` cells, and a list of `steps`. A job with `"resume": true` continues the previous world "without ticking". — [PdKernel.java L59-63, L167-204](<grader/kernel/src/pd/PdKernel.java>)
- **Ops:**
  - `clear` empties the scan box and drains 100 ticks.
  - `place` takes any block-state strings. Blocks go down silently first, then shape updates and neighbour updates run in (x, y, z) order. Observers skip their own placement update unless `observers_fire_on_place` is set.
  - `lever` pulls a lever and records the instant dust changes.
  - `run` steps with `max_ticks`, `min_ticks`, `quiet` (stop after N ticks with no change) and `max_changes`.
  - `snapshot` lists every non-air cell.
  - [PdKernel.java L182-189, L291-425](<grader/kernel/src/pd/PdKernel.java>)
- **Per-tick output of a `run` step:**
  - `door`: one string per tick, with `#` door block, `.` air, `m` moving piston, `?` other.
  - `changes`: `[tick, x, y, z, old_state, new_state]` for every cell whose block state changed. The default cap is 600 per step (`MAX_CHANGES`), overridable with `max_changes`.
  - `ticks`, `last_change_tick`, `quiescent`, `moving_at_end`, and the swept bounding box.
  - Per job: `entity_seen`, `frozen_violation` and `escaped`.
  - [PdKernel.java L65-67, L366-408, L433-510](<grader/kernel/src/pd/PdKernel.java>)
- **What it does not report.** The kernel reports block-state diffs. It does not dump Minecraft's internal block-event queue or scheduled-tick queue. Piston motion is visible as `moving_piston` states and `extended=` changes. — [PdKernel.java L433-471](<grader/kernel/src/pd/PdKernel.java>)
- **Grading job.** `build_job` places the hallway shell and the design, settles for up to 60 ticks (`SETTLE_CAP` 40 plus `QUIET` 20), then runs the cycles. Each flip is a lever pull, a move phase capped at 200 + 20 ticks, and a 40-tick hold. There are 3 cycles in dev mode and 8 in final mode, where final mode adds idle delays of 0-29 ticks before each flip. — [grader/pdgrader/grade.py L34-69](<grader/pdgrader/grade.py>); [grader/pdgrader/rules.py L19-27](<grader/pdgrader/rules.py>)
- **Rules checked in `grade.py`.** It checks settle, initial state, open and close within `TIME_CAP`=200, `too_slow`, the hold, entities (item drops), hallway and wall intrusion, leaving the test volume, and seamless ring visibility. Volume is the swept bounding box. — [grade.py L114-209](<grader/pdgrader/grade.py>)
- **Allow-list.** It has 19 plain cubes (stone, smooth stone, iron, 16 concretes) plus 18 components: piston, sticky_piston, piston_head, redstone_wire, repeater (delay 1-4), comparator, redstone_torch, redstone_wall_torch, redstone_block, observer, slime, honey, target, note_block, lever, obsidian, glass and white_glazed_terracotta. — [rules.py L118-157](<grader/pdgrader/rules.py>)
- **Agent-facing tools.**
  - `test` returns a verdict line such as "VALID. volume V (w x h x d), blocks B, open X ticks, close Y ticks, at rest by tick Z". On failure it lists FAIL codes, a doorway timeline (`t0 ###/###/###`) and up to 30 first block changes.
  - `trace` prints lines like `t=3 (x,y,z) sticky_piston[...] -> moving_piston[...]` per flip. The display defaults to 80 lines, and kit 1 is capped at 600 changes per flip.
  - [grader/pdgrader/session.py L32-52, L206-307](<grader/pdgrader/session.py>); [grader/README.md "Kit versions"](<grader/README.md>)
- **Kit 2 adds `film`.** It is the whole run as data (every tick of every flip, up to 20,000 changes) with a `Film` class (`f.at(flip, t)`, cell history). — [grader/README.md "Kit versions"](<grader/README.md>)
- **The lab.** It places arbitrary allow-listed blocks (any number of levers), flips levers, and steps exact ticks or runs until at rest. Every call rebuilds the world deterministically by replaying all prior ops. One lab world is capped at 4,000 ticks. — [grader/README.md "The lab and the Python session"](<grader/README.md>); [session.py L20](<grader/pdgrader/session.py>)
- **Changed physics.** `PhysicsAgent.java` is a `-javaagent` that uses the JDK ClassFile API to swap integer constants:
  - `repeater_unit`: constant 2 in `RepeaterBlock.getDelay`, 1 site.
  - `push_limit`: constant 12 in `PistonStructureResolver`, 3 sites.
  - `observer_delay`: constant 2 in `ObserverBlock.startSignal`, only where the next instruction calls `scheduleTick`, 1 site.
  - `observer_pulse`: constant 2 in `ObserverBlock.tick` before `scheduleTick`.
  - Each patch must match the expected site count or the JVM halts, and the kernel refuses to start unless every requested key printed `PDK_PHYSICS`.
  - [grader/kernel/agent/pd/PhysicsAgent.java L19-41, L84-123](<grader/kernel/agent/pd/PhysicsAgent.java>); [kernel.py L149-171](<grader/pdgrader/kernel.py>)
- **One physics setting per JVM.** A simulator runs a single physics setting, and `serve-many` starts one simulator per distinct setting. — [grader/README.md "Changed physics"](<grader/README.md>)
- **Parity.** `tests/parity_dedicated.py` matched the kernel against a dedicated server stepped with `/tick step 1`. It covered 2 contraptions (31 and 5 cells) over 16 ticks each, with an exact match. — [grader/README.md "What has been verified"](<grader/README.md>)

### Inferences
- The kernel already supports what a search program needs: load an arbitrary layout, step tick by tick, and read back per-tick cell diffs and the doorway pattern. A non-LLM optimizer can call `pdgrader.grade.grade(kernel, design, n, track, mode)` directly in Python with no tool server. I did this for the measurements below.
- Changed physics changes timing constants, not the rules. Only those four constants can be changed: comparators, torches and piston stroke time are not patchable, per the README.

### Gaps
- The kernel exposes no internal event queues (block events, scheduled ticks), only resulting state changes. A search that needs update-order detail would have to infer it.
- Parity with ordinary Minecraft has been shown for only two small contraptions.

## 2. Speed: wall-clock per verification, ticks simulated, and evaluations per hour

### Takeaway
On this M4 laptop, one simulator grades a small 3×3 or 4×4 door in dev mode (3 cycles, about 640-980 ticks) in about 0.08-0.2 s. Final mode (8 cycles, about 1,650-2,570 ticks) takes about 0.23-1.2 s. The full check of final mode plus 11 extra placements takes about 2.7-4.4 s. That is roughly 36,000 dev evaluations per hour per simulator. For comparison, all 58 agent runs together made 457 test calls.

### Cited Findings
- **Simulator boot (measured):** 5.0-5.4 s for vanilla and single-change physics, 6.2 s for `observer_delay=3`, and 8.7 s for `repeater_unit=3,observer_delay=3`. The README says "about 4 s to start". — [measured, timing.json](<../../runs/bench/search_pilot/timing.json>); [grader/README.md "Use"](<grader/README.md>)
- **Wall-clock and ticks per design (measured).** Dev timings are four repeated gradings on one warm simulator. Tick counts include the 100-tick clear drain.

| Design | Dev wall (s) | Final wall (s) | Ticks, dev / final |
|---|---|---|---|
| Fable 3×3, volume 70 (`w1-fable-a`) | 0.34-0.84 | 0.36 | 684 / 1,783 |
| Opus 3×3, volume 80 (`w3-opus-d`) | 0.09-0.20 | 0.47 | 768 / 2,007 |
| Opus 4×4, volume 240 (`w4-4x4-opus-e`) | 0.14-0.16 | 0.48 | 792 / 2,071 |
| Fable 4×4, volume 264 (`w2-4x4-fable-a`) | 0.14-0.19 | 0.50 | 960 / 2,519 |
| Opus 4×4, volume 5,236 (`w2-4x4-opus-b`) | 0.45-0.53 | 1.16 | 978 / 2,567 |

  — [measured, timing.json](<../../runs/bench/search_pilot/timing.json>)
- **Robustness check (final grade at 11 other placements, measured):** 3.15 s for the Fable 70 and 3.93 s for the Opus 240 4×4. Delay variants of the Fable 70 took 2.7-4.4 s for final mode plus placements. — [measured, timing.json and verify.py output](<../../runs/bench/search_pilot/timing.json>)
- **Measured sweep throughput:** 16 delay variants of the Fable 70 graded in dev mode took 1.46 s (0.091 s each) on vanilla and 1.34 s (0.083 s each) under changed physics. — [measured, timing.json "sweep_w1-fable-a"](<../../runs/bench/search_pilot/timing.json>)
- **Whole measurement script:** about 66 s wall-clock and about 147 CPU-seconds (user plus sys) for 4 simulator boots and roughly 150 gradings. That averages about 2.2 cores busy for one simulator process at a time. — [measured, `time` output of timeit.py](<../../runs/bench/search_pilot/timeit.py>)
- **README timings:** "about 50 ms per dev grading natively, about 100 ms in a Linux container", and "about 50 ms for a small door, 150 ms in final mode". One shared simulator uses about 450 MB. — [grader/README.md "Use", "Several runs at once", "What has not"](<grader/README.md>)
- **Agent usage for comparison.** Across all 58 finished runs, agents made 457 test calls (median 5, max 82) and 370 trace calls. Lab ticks per run had a median of 943 and a max of 50,000. — [runs/bench/dashboard/runs.json](<runs/bench/dashboard/runs.json>)
- **Agent usage on the 70 doors.** `w1-fable-a` reached its 70 door with 22 tests in a 120-minute run that cost $47.21. `w8-3x3-chg-b-opus` used 2 tests and 19 traces. — [runs/bench/dashboard/runs.json](<runs/bench/dashboard/runs.json>)
- **The kernel can't stop early.** `grade()` sends the whole multi-cycle job to the kernel and only then checks it, so a failed design still simulates all cycles. — [grade.py L108-111](<grader/pdgrader/grade.py>)
- **Fixed waiting per flip.** `QUIET`=20 and `HOLD`=40 add at least about 60 ticks to every flip regardless of how fast the door is. — [rules.py L19-22](<grader/pdgrader/rules.py>); [grade.py L53-57](<grader/pdgrader/grade.py>)

### Inferences
- **One simulator:**
  - Small 3×3 door in dev mode (about 0.1 s): about 36,000 evaluations per hour.
  - Small 4×4 door in dev mode (0.14-0.19 s): about 20,000-25,000 per hour.
  - Final mode: about 3,000-15,000 per hour.
  - Full robustness verification (about 3-4 s): about 1,000 per hour.
- **Several simulators.** One simulator averaged about 2.2 cores and uses about 450 MB. Four or five independent `Kernel` processes on the 10-core, 16 GB M4 could plausibly reach about 100,000-180,000 dev evaluations per hour. I have not measured this. `Kernel.run_job` holds a lock, so one process serialises its jobs.
- **Possible speed-ups.** Stopping at the first failed flip, or a cheaper screening mode (1 cycle, shorter QUIET and HOLD), would likely cut the cost of a failing candidate by 2-3×. Both would be grader changes.
- **Scale.** One hour of brute-force evaluation is about 80× all agent test calls in the benchmark combined.

### Gaps
- I did not run several simulators in parallel, so the multi-process figure is an estimate.
- Timings vary from run to run: the Fable 70 dev grade ranged 0.34-0.84 s while other 3×3 doors took about 0.1 s. Background load on the laptop was not controlled.

## 3. Best designs: block counts, tunable parameters and search-space size

### Takeaway
The smallest doors are very sparse. The Fable 70 3×3 has 47 blocks with only 2 repeaters (16 delay combinations). The Opus changed-physics 70 has 48 blocks and 1 repeater (4 combinations). The smallest 4×4 found is not a Fable door: it is Opus's 240 (`w4-4x4-opus-e`), with 118 blocks and 10 repeaters (about 1.05 million combinations). The Opus 5,236 4×4 is the largest working 4×4: 911 blocks, 183 repeaters, 4^183 ≈ 10^110 combinations. Delay-only search spaces are tiny for the best doors. The layout space is astronomically large: about 10^91 for a 70-cell box with 20 block choices per cell.

### Cited Findings
- **Block counts** come from each run's `result.json` "candidate" (the design that passed the final grade). "Blocks" is the grader's `block_count`, which excludes the lever. "Stone" includes the 9 or 16 door blocks. — [runs/bench/w*/<run>/result.json](<runs/bench/>); [measured, blocks.py](<../../runs/bench/search_pilot/blocks.py>)

| Door (run) | Physics | Volume (dims) | Blocks | Sticky pistons | Pistons | Observers | Repeaters (delays) | Dust | Stone | Other | Blocks with a facing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Fable 3×3 70 (`w1-fable-a`) | vanilla | 70 (7×10×1) | 47 | 10 | 0 | 4 | 2 (both 4) | 8 | 21 | target 1, note_block 1 | 17 |
| Opus 3×3 70 (`w8-3x3-chg-b-opus`) | rep 3, obs 3 | 70 (7×10×1) | 48 | 10 | 0 | 11 | 1 (3) | 7 | 18 | note_block 1 | 23 |
| Fable 3×3 72 (`w5-3x3p-fable-a`) | rep 3, obs 3 | 72 (8×9×1) | 61 | 10 | 1 | 34 | 2 (4, 2) | 0 | 13 | obsidian 1 | 48 |
| Fable 3×3 72 (`w5-3x3p-fable-b`) | rep 3, obs 3 | 72 (9×8×1) | 58 | 11 | 0 | 26 | 1 (4) | 4 | 15 | glass 1 | 39 |
| Opus 3×3 80 (`w3-opus-d`) | vanilla | 80 (8×10×1) | 66 | 10 | 0 | 36 | 1 (4) | 2 | 17 | – | 48 |
| Opus 4×4 240 (`w4-4x4-opus-e`) | vanilla | 240 (10×8×3) | 118 | 20 | 0 | 44 | 10 (8×1, 2×4) | 12 | 32 | – | 75 |
| Fable 4×4 264 (`w2-4x4-fable-a`) | vanilla | 264 (11×8×3) | 164 | 20 | 0 | 91 | 5 (all 1) | 15 | 28 | glass 5 | 117 |
| Opus 4×4 5,236 (`w2-4x4-opus-b`) | vanilla | 5,236 (34×11×14) | 911 | 20 | 0 | 42 | 183 (111×1, 2×2, 8×3, 62×4) | 257 | 301 | glass 94, obsidian 6, slime 4, honey 4 | 246 |

- **There is only one Fable 70 door, `w1-fable-a` (wave 1, vanilla).** Fable's best changed-physics doors are the two 72s in wave 5. The other 70 is Opus's changed-physics door from wave 8. — [runs/bench/dashboard/runs.json](<runs/bench/dashboard/runs.json>); [runs/bench/w8/RESULTS.md](<runs/bench/w8/RESULTS.md>)
- **The 13 Nov report is out of date on 4×4.** It gives the best 4×4 doors as Fable 264 and Opus 2,574. Waves 4 and 7 came later. Wave 4 produced Opus 240 (`w4-4x4-opus-e`, the smallest 4×4 overall) and Opus 1,430. — [reports/Piston Door Bench results.md "The size ladder"](<reports/Piston Door Bench results.md>); [runs/bench/dashboard/runs.json](<runs/bench/dashboard/runs.json>)
- **Allowed repeater delays are 1-4.** Facings are 6-way for pistons and observers and 4-way for repeaters, comparators and wall torches. — [rules.py L136-157](<grader/pdgrader/rules.py>)
- **Naive parameter-space sizes for a fixed layout.** The figures cover repeater delays, plus all facings and comparator modes. The layout figure assumes about 20 functionally distinct choices per bounding-box cell (air, one plain cube and 18 components), ignoring orientation.

| Door | Delay combinations | Delays + facings + modes | Layout space |
|---|---|---|---|
| Fable 70 | 4^2 = 16 | about 10^13 | about 10^91 |
| Opus changed-physics 70 | 4^1 = 4 | about 10^17.5 | about 10^91 |
| Opus 80 | 4 | about 10^37 | – |
| Opus 4×4 240 | 4^10 = 1,048,576 | about 10^62 | about 10^312 |
| Fable 4×4 264 | 4^5 = 1,024 | about 10^92 | – |
| Opus 4×4 5,236 | 4^183 ≈ 10^110 | about 10^269 | – |

  — [measured, space.py](<../../runs/bench/search_pilot/space.py>)
- **Delay sweep on the Fable 70 (measured, vanilla, all 16 combinations).** The repeaters are at (2,-3,0) facing east and (2,5,0) facing west.
  - Only 3 of 16 combinations work: (4,2), (4,3) and the original (4,4).
  - Any first-repeater delay below 4 fails: `did_not_close` when the second delay is 1, and `did_not_open` otherwise.
  - In final mode, (4,2) opens in 30 and closes in 18 ticks, against the original's 34 and 22. It passes all 11 placements at the same volume of 70.
  - [measured, timing.json "sweep_w1-fable-a" and verify.py](<../../runs/bench/search_pilot/verify.py>)
- **Delay sweep on the Opus changed-physics 70 (measured).**
  - Under its own physics, delay 3 (the original) gives open/close 38/26, delay 4 gives 44/29, and delays 1 and 2 fail.
  - Under vanilla physics no delay works (0 of 4, all `did_not_close`).
  - [measured, timing.json](<../../runs/bench/search_pilot/timing.json>)

### Inferences
- **Delay tuning can't shrink a door.** On a fixed layout it leaves the bounding box unchanged. For the smallest doors it is fully enumerable in about 1-2 s and can only improve speed, robustness or validity. The Fable 70 sweep found a 4-tick-faster variant at the same volume, so a cheap sweep finds real improvements on an existing door.
- **Shrinking needs layout moves.** Adding, removing, moving or turning blocks is where the space explodes (10^91 and up), so a search program needs strong structure. Plausible sources are templates, the doorway and piston skeleton (10 sticky pistons for every 3×3 door, 20-24 for 4×4), and local edits seeded from agent doors.
- **Delay-only enumeration stays cheap up to about 4^10.** For the Opus 240 4×4 that is about 1.05 M evaluations, about 41 hours on one simulator at about 0.14 s. Beyond that it needs a smarter method, such as tick-by-tick constraint propagation from traces or coordinate descent.

### Gaps
- My block taxonomy counts submitted blocks. It does not separate structural stone from door blocks, and it does not measure which blocks are actually needed. No ablation (removing each block in turn) was run.
- Facing combinations were counted naively; most are physically meaningless.

## 4. Fact-checking three claims about the results

### Takeaway
(a) is true for the benchmark's changed-physics setting (repeater step 3 and observer delay 3), but false if "modified timings" means repeater step 3 alone. (b) reproduces exactly (89.1%), but only under one specific definition that the late first doors of two Opus runs dominate. (c) is out of date: 52 was the count through wave 7, and the current count is 58 finished runs.

### Cited Findings
- **(a) "Fable's 70-volume 3×3 door works under vanilla rules and fails under your modified timings."**
  - The only Fable 70 is `w1-fable-a`. Under vanilla it is valid in dev and final mode (open 34, close 22 ticks) and passes all 11 placements.
  - Under `repeater_unit=3,observer_delay=3` (the wave 5/8 changed-physics task) it fails in both dev and final mode: `did_not_open` on cycle 1, with the doorway at the end showing `.../.../.#.` (one cell stuck closed).
  - Under `observer_delay=3` alone it fails the same way.
  - Under `repeater_unit=3` alone it is valid, with open 46 and close 30 ticks.
  - No repeater-delay setting rescues it under the combined change (0 of 16).
  - [measured, timing.json](<../../runs/bench/search_pilot/timing.json>)
  - **Consistency with the README.** The README table reports `repeater_unit=3`: "6 of 15 (best 70)" and `repeater_unit=3,observer_delay=3`: "6 of 15 (best 80)". This fits the Fable 70 surviving the repeater change but not the combined change. — [grader/README.md "Changed physics"](<grader/README.md>)
  - **Verdict:** TRUE for the benchmark's changed-physics task. FALSE if the claim means the repeater-only change. The observer-delay change alone is enough to break it.
- **The mirror case.** The Opus changed-physics 70 (`w8-3x3-chg-b-opus`) fails under vanilla (`did_not_close`, cycle 1), so neither 70 transfers between the two worlds. — [measured, timing.json](<../../runs/bench/search_pilot/timing.json>)
- **(b) "On 4×4 doors, 89% of the observed improvement in log volume came after the first hour among the eight runs that produced working doors."**
  - **Data.** Exactly 8 kit-1 4×4 runs produced doors: w2 Fable a and b, w2 Opus a and b, w4 Fable e and f, w4 Opus e and f. Wave 7 kit 2 adds 6 more.
  - **Method.** Improvement is the pooled log(first-door volume ÷ final volume), with the cut at 60 working minutes from `curve.json`.
  - **Result.** Total 6.965, of which 6.209 came after 60 minutes, or **89.1%**.
  - **Caveat 1: late first doors.** Three runs found their first door after minute 60: `w2-4x4-opus-a` at 98.2 min, `w2-4x4-opus-b` at 114.0 and `w4-4x4-fable-f` at 60.1. All of their improvement counts as after the hour by construction, which is 3.395 of the 6.209.
  - **Caveat 2: concentration.** The two w2 Opus runs alone are 46% of the total.
  - **Without the 3 late-first-door runs:** 78.8%.
  - **Per run:** 6 of 8 runs had 100% of their improvement after 60 minutes, `w4-4x4-fable-e` had 64%, and `w4-4x4-opus-e` (the 240) had 0%: it reached 240 by minute 60 and never improved after.
  - **Including the kit-2 4×4 runs (14 runs):** 83.7%. Three of those (the wave 7 Fable runs) were stopped by the harness at 68 of 150 minutes.
  - **For contrast:** standard 3×3 runs (15 doors) show 54.1%.
  - [runs/bench/dashboard/curve.json, runs.json](<runs/bench/dashboard/curve.json>); [measured, claim_b.py](<../../runs/bench/search_pilot/claim_b.py>); [runs/bench/w7/manifest.json](<runs/bench/w7/manifest.json>)
  - **Verdict:** TRUE as a computation (89.1%), but fragile. It depends on pooling, on the kit-1-only subset, and on counting improvement from the first working door, and it is driven by two Opus runs whose first door came after the hour.
- **Separate statistic in the report.** The report itself says "about a quarter of the improvement came after the first continue message". That cuts at the first continue message, not at 60 minutes, and covers runs through 13 Nov. — [reports/Piston Door Bench results.md, Finding 3](<reports/Piston Door Bench results.md>)
- **(c) "Across 52 runs…"**
  - The manifests list 62 runs: w1 8, w2 8, w3 8, w4 12, w5 6, w6 4, w7 10, w8 6.
  - Wave 7 has 2 Fable 3×3 kit-2 runs "cancelled… not a result, exclude from analysis" and 2 Opus 3×3 runs "held: not launched". That leaves 58 finished runs, and `dashboard/runs.json` has exactly 58 entries.
  - Waves 1-7 alone have 8+8+8+12+6+4+6 = 52 finished runs, so 52 is the count from before wave 8's 6 runs.
  - [runs/bench/w*/manifest.json](<runs/bench/w7/manifest.json>); [runs/bench/dashboard/runs.json](<runs/bench/dashboard/runs.json>)
  - **Verdict:** FALSE for the current data (out of date by wave 8). Any statistic quoted "across 52 runs" leaves out the wave 8 Opus 3×3 runs, including the changed-physics 70.

### Inferences
- Claim (a) is better stated as: "the Fable 70 survives a slower repeater but not a slower observer". Its timing depends on observer timing, which fits its 4 observers and 10 sticky pistons in a single layer.
- For (b), a more robust phrasing is per run. In 6 of the 8 kit-1 4×4 runs, all improvement from the first working door came after the first hour, partly because 3 runs only found a first door after the hour.

### Gaps
- The exact definition the other AI used for (b) is unknown. I reproduced 89.1% under the most natural definition (pooled log ratio, working minutes, kit 1).
- "First hour" here means working minutes as recorded by `analyze.py`, with sleep windows excluded, not wall-clock time.

## 5. Is opening and closing speed already measured?

### Takeaway
Yes. Every valid grade reports `open_ticks`, `close_ticks` and `reset_ticks`, and agents see them in every `test` reply. They are diagnostics and are not part of the score. Doors must open or close within 200 ticks.

### Cited Findings
- **How the speeds are defined.**
  - For each flip, `reach_tick` is the first tick after which the doorway pattern stays at the target for the rest of the move phase. The lever flips at t=0.
  - `reset_tick` is the last tick with any block change.
  - `open_ticks` and `close_ticks` are the maximum `reach_tick` over all opening and all closing flips. `reset_ticks` is the maximum `reset_tick`.
  - A door that is not quiet by the 200-tick `TIME_CAP` fails as `too_slow`.
  - [grade.py L150, L161-169, L216-219](<grader/pdgrader/grade.py>); [rules.py L19](<grader/pdgrader/rules.py>)
- **Agents see the speeds.** The `test` reply shows "open X ticks, close Y ticks, at rest by tick Z", and the run log records `open_ticks` and `close_ticks` per test. — [session.py L220-227](<grader/pdgrader/session.py>)
- **Final-grade speeds (8 cycles, from result.json), in ticks:**

| Door (run) | Physics | Open | Close |
|---|---|---|---|
| Fable 3×3 70 (`w1-fable-a`) | vanilla | 34 | 22 |
| Opus 3×3 70 (`w8-3x3-chg-b-opus`) | changed | 38 | 26 |
| Fable 3×3 72 (`w5-3x3p-fable-a`) | changed | 77 | 77 |
| Fable 3×3 72 (`w5-3x3p-fable-b`) | changed | 90 | 60 |
| Opus 3×3 80 (`w3-opus-d`) | vanilla | 46 | 46 |
| Fable 3×3 140 (`w3-fable-c`) | vanilla | 40 | 16 |
| Opus 4×4 240 (`w4-4x4-opus-e`) | vanilla | 52 | 40 |
| Fable 4×4 264 (`w2-4x4-fable-a`) | vanilla | 90 | 66 |
| Opus 4×4 396 (`w7-4x4k2-opus-c`) | vanilla | 82 | 82 |
| Opus 4×4 5,236 (`w2-4x4-opus-b`) | vanilla | 86 | 63 |
| 2×2 30 doors | vanilla | 1 | 3 |
| 3×2 42 doors | vanilla | 7, 9, 17, 21 | same as open |

  — [runs/bench/w*/<run>/result.json](<runs/bench/>); [measured, blocks.py](<../../runs/bench/search_pilot/blocks.py>)
- **Re-measured speeds.** My measured `reset_ticks` were 36 (Fable 70), 48 (Opus 80), 54 (Opus 240) and 92 (Fable 264).
  - Under changed physics the Opus 80 slows to 68/68 ticks, and the Fable 70 slows to 46/30 under the repeater-only change.
  - [measured, timing.json](<../../runs/bench/search_pilot/timing.json>)
- **The community 4×4 claim** quoted in the references is a "no-entity 0.9 s 4x4", which is 18 ticks. It is self-reported and was not rebuilt here. — [grader/pdgrader/references.py L28](<grader/pdgrader/references.py>)

### Inferences
- The best agent 4×4 doors take 40-90 ticks (2-4.5 s). The community claims 0.9 s, so a speed objective has large headroom.
- Volume versus speed is a natural two-objective front: the Fable 140 3×3 closes in 16 ticks against 22 for the Fable 70. A delay sweep already moved the Fable 70 to 30/18 at the same volume.

### Gaps
- Speed is not part of the score, and agents were never asked to optimise it, so these numbers are by-products.
- `open_ticks` measures doorway completion, not when the hallway is passable.

## 6. Minimal code changes for (i) a repeater-delay sweep optimizer and (ii) a "repair" environment

### Takeaway
(i) needs no grader change: a script of about 30 lines that edits `props["delay"]` on repeater blocks and calls `grade()` on one `Kernel` per physics setting does it. I wrote and ran one. (ii) can reuse the existing `improve` variant, which already hands an agent a `start.json`. It needs a perturbation generator, a new variant name with its own brief paragraph (the current one says the start design is "valid"), per-instance starting files, and a repair-specific score.

### Cited Findings
- **(i) Python entry points:**
  - `Kernel(physics=...)` is a context manager, one per physics setting.
  - `grade(kernel, sub, n, track, mode)` returns `valid`, `failures[].code`, `volume`, `open_ticks`, `close_ticks`, `reset_ticks`, `partial` and `flips_passed`.
  - `translation_pass_rate(...)` checks 11 placements.
  - A design is `{"initial_state", "blocks":[{"pos","id","props"}]}`, and repeater `delay` must be "1"-"4".
  - [kernel.py L146-233](<grader/pdgrader/kernel.py>); [grade.py L87-271](<grader/pdgrader/grade.py>); [rules.py L139](<grader/pdgrader/rules.py>); [grader/README.md "Use"](<grader/README.md>)
- **(i) Working prototype:** `runs/bench/search_pilot/timeit.py` and `verify.py` do itertools.product over delays, grade in dev mode, then re-check winners in final mode with placements. The only workaround needed: `Kernel` makes its scratch world under `grader/runtime/`, which I redirected to a temp folder by patching `pdgrader.kernel.tempfile`. — [kernel.py L156](<grader/pdgrader/kernel.py>); [measured, timeit.py](<../../runs/bench/search_pilot/timeit.py>)
- **(i) Optional grader hooks for speed:**
  - Abort after the first failed flip. `build_job` emits all cycles up front, and `grade` checks only after `run_job`.
  - Make `QUIET`, `HOLD` and `CYCLES` parameters for a cheap screening pass. They are now module constants.
  - Run several `Kernel` processes, since `run_job` holds `_job_lock`.
  - [grade.py L34-69, L108-111](<grader/pdgrader/grade.py>); [rules.py L19-23](<grader/pdgrader/rules.py>); [kernel.py L172, L195-197](<grader/pdgrader/kernel.py>)
- **(i) Richer objectives** can come from the kernel's per-tick `door` strings and `changes`. Examples are partial credit (`partial`, `cells_reached`) and timing of individual piston moves. A wider search could use `film`-level detail by raising `max_changes` on `run` steps, as `session._sim` does. — [session.py L258-271](<grader/pdgrader/session.py>); [PdKernel.java L370](<grader/kernel/src/pd/PdKernel.java>)
- **(ii) Existing improve variant:**
  - `serve --variant improve --starting <file> --starting-volume V` writes `start.json` into the kit via `kit.make_kit(..., starting, volume)`.
  - The brief inserts the `STARTING` text: "`start.json` is a working design … valid but large".
  - `references.STARTING` maps (n, track) to a file.
  - The Inspect task builds `improve` samples from `references.starting`.
  - [grader/pdgrader/__main__.py L89-118, L128-131](<grader/pdgrader/__main__.py>); [grader/pdgrader/kit.py L481-486, L528-568](<grader/pdgrader/kit.py>); [references.py L34-71](<grader/pdgrader/references.py>); [grader/inspect_task/piston_door.py L278-297](<grader/inspect_task/piston_door.py>)
- **(ii) Constraints on changes:**
  - Kit 1 brief text is frozen and checked byte for byte, so a new variant must add text only when that variant is selected.
  - Sessions log `variant` and restore it on resume.
  - `score()` grades the last submission in final mode and reports volume and score against the reference.
  - [grader/README.md "Kit versions"](<grader/README.md>); [session.py L54-88](<grader/pdgrader/session.py>); [grader/pdgrader/server.py L103-124](<grader/pdgrader/server.py>)
- **(ii) Ready-made perturbations from this session's measurements:**
  - The Fable 70 with repeater delays changed fails in 13 of 16 settings, with known failure codes (`did_not_open`, `did_not_close`).
  - The Fable 70 under `repeater_unit=3,observer_delay=3` fails, and no delay change fixes it. This makes it a "port this door to the new physics" task that needs a structural edit.
  - The Opus changed-physics 70 under vanilla fails, and no delay fixes it either.
  - [measured, timing.json](<../../runs/bench/search_pilot/timing.json>)

### Inferences
- **Minimal plan for (ii):**
  1. Write a `perturb(design, kind, rng)` helper (delay change, facing flip, block delete or move, block swap). Keep only perturbations where `grade()` fails and the original passes. Optionally check that one inverse edit restores validity.
  2. Add `"repair"` to the `--variant` choices and add a `STARTING_REPAIR` text to `kit.py` saying the design is broken and naming the task's physics.
  3. Pass `--starting` per instance. This needs no `references.py` change, since `--starting` already exists.
  4. In `score()`, report repaired (valid), the number of edited cells versus the original, and the volume change. These would be new fields in `server.score`.
  5. For Inspect, add repair samples with `start_path` in metadata alongside the `improve` branch in `piston_door.py`.
- **Physics-port repair** needs no perturbation code at all. Launching the existing improve variant with `physics={"repeater_unit":3,"observer_delay":3}` and the vanilla Fable 70 as `--starting` gives a broken start, which is a real repair task. Only the brief wording ("valid but large") is wrong for it. The `serve` CLI does accept `--physics` together with `--starting`, which implies `--variant improve`: both are passed to `kit.make_kit` and `server.serve` ([__main__.py L85-119](<grader/pdgrader/__main__.py>)). I have not run this combination.

### Gaps
- I did not implement or test either environment. For (ii), I did not check how `score()` treats a run whose start design is invalid.
- How hard a repair task is (how many edits are needed) was not measured beyond the delay-only sweeps above.
