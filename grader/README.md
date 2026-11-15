# pdgrader

Grades a piston-door design against rulebook v0.3 (`../phase0/RULEBOOK-v0.md`) by running it
in unmodified Minecraft Java 26.3.

## Setup

Needs a JDK 25 and the Minecraft 26.3 `server.jar` (download it from Mojang; it is not shipped here).

```bash
python3 -m pdgrader setup --java-home <jdk-25-home> --server-jar <server.jar>
```

This unpacks the server's bundled libraries into `runtime/`, compiles the kernel into
`kernel/build/<hash of the source>/`, and writes `config.json`. All three are generated and can
be deleted. If the kernel source changes it is recompiled into a new folder on next use, so a
simulator that is already running is never disturbed.

## Use

```bash
python3 -m pdgrader grade fixtures/good_2x2.json --n 2 --track seamless
```

- `--track open|seamless`: which visibility rule applies.
- `--final`: 8 cycles instead of 3, varied flip timing, and a fresh simulator per file.
- `--translations`: also report how many of 11 other placements still pass (8 shifts, 3 half turns).
- `--reference <volume>`: report a score (reference ÷ volume).
- `--json`: full result, including per-failure detail (doorway timeline, first block changes).

Exit code is 0 only if every file is valid.

From Python, keep one simulator alive across many gradings:

```python
from pdgrader.kernel import Kernel
from pdgrader.grade import grade

with Kernel() as k:                      # about 4 s to start
    result = grade(k, submission, n=3, track="seamless")   # about 50 ms for a small door, 150 ms in final mode
```

A submission is `{"initial_state": "open"|"closed", "blocks": [{"pos": [x, y, z], "id": "piston", "props": {"facing": "east"}}]}`.
Doorway cells are `(x, y, 0)` for `0 <= x, y < n`; the hallway runs along z.
`fixtures/make_fixtures.py` shows complete examples.

### Door shapes

`--n` takes a square size (`3`) or a rectangle written width x height (`3x2`: 3 cells along x,
2 along y). In Python and in specs a size is an int or a `[w, h]` pair. Square sizes are always
stored as an int, so logs, references and briefs for the square tasks are exactly as before
(the briefs were diffed byte for byte after the change). A rectangular brief adds one sentence
naming which side is the width. Width and height are not interchangeable: a 2x1 door is not a
valid 1x2 door. Sides run 1 to 7.

### Kit versions

Kit 1 is the brief and tools every run in benchmark waves 1 to 6 used; its text is frozen and
checked byte for byte. `--kit-version 2` (or `"kit_version": 2` in a spec) gives the agent kit 2,
which adds three things and changes nothing else:

- **The film.** `./pd film design.json` (Python: `film(design)`) runs the design as `trace` does
  and returns the whole run as data: the build at rest, then every tick of every flip with the
  doorway and each block change, plus any entity or protected-cell violation. The `Film` class
  gives the state of every block at any tick (`f.at(flip, t)`), one cell's history, the doorway
  timeline and a search over changes. It costs one trace/view call. Kit 1's `trace` is text
  only and reports at most 600 changes per flip; the film reports up to 20,000.
- **Structured test results** in Python: `r.bbox`, `r.block_count`, `r.timings`, `r.detail`.
- **Thirteen added statements in the brief**, each one reported missing by an earlier run:
  eleven component facts and two rule details. `tests/test_kit2.py` asserts every one.

The kit version is recorded in the run log; a kit-1 session answers `film` with "unknown tool"
and a kit-1 folder contains no mention of it. Kit 2's extra files live in `kit_template_v2/`
and are copied over the kit-1 files. The Inspect interface gets the added facts but not the film yet.

### Changed physics

`--physics key=value,...` (or `"physics": {...}` in a spec, or `Kernel(physics=...)`) runs the game
with some constants changed. A Java agent (`kernel/agent/pd/PhysicsAgent.java`) rewrites them in
Minecraft's own classes as they load; the server jar on disk is never modified.

| Setting | Vanilla | Where it is patched |
|---|---|---|
| `repeater_unit` | 2 | ticks per repeater delay step (`RepeaterBlock.getDelay`) |
| `push_limit` | 12 | most blocks a piston moves (3 sites in `PistonStructureResolver`) |
| `observer_delay` | 2 | ticks from a watched change to the output (`ObserverBlock.startSignal`) |
| `observer_pulse` | 2 | ticks the output stays on (`ObserverBlock.tick`) |

Every patch must find exactly the constants it expects, and every requested setting must report
itself applied before the kernel counts as started; otherwise the kernel refuses to start. Runs
record their physics in the log, a resumed run must have the same physics, the final test uses
a simulator with the run's physics, and vanilla references never apply to changed physics.
`serve-many` gives each distinct physics setting its own simulator.

The brief states the changed values in a short paragraph and in the component facts, which are
rendered from the settings. Vanilla settings render the original text exactly. Only behaviour
that was measured is stated: an observer pulse of 4 lets a sticky piston finish its push and
pull its block back (no block dropping); a pulse of 3 has not been measured, so the brief refuses it.

How much it changes, measured on the 23 working doors from the pilot and benchmark waves 1-3:

| Physics | Doors still working | 3×3 doors still working |
|---|---|---|
| `push_limit=8` | 23 of 23 | all |
| `observer_delay=3` | 19 of 23 | 12 of 15 |
| `repeater_unit=3` | 13 of 23 | 6 of 15 (best 70) |
| `repeater_unit=3,observer_delay=3` | 13 of 23 | 6 of 15 (best 80) |
| all four (`3, 8, 3, 4`) | 6 of 22 | 0, including the 1430 existence proof |

So compact doors depend on exact timings. With all four changes no 3×3 door is yet known to
exist; with `repeater_unit=3,observer_delay=3` several do, so that is the solvable changed-physics task.

## Running an agent against it

One tool server per agent run. It owns the simulators, the budgets and a log the agent
never sees; the agent talks to it only through its tools.

```bash
python3 -m pdgrader serve --n 3 --track seamless --port 8811 --log runs/x/log.jsonl --kit runs/x/kit
```

`--kit` writes the agent's working folder: `TASK.md` (the full brief), the `pd` client,
`pdbuild.py` (a design-building helper), `pdlab.py` (the tools as a Python module) and two
examples. `--variant improve` also hands over `start.json`, a working but bulky door to
shrink (only for tasks that have one in `pdgrader/references.py`); the default, `scratch`,
starts from nothing. Budgets are `--tests` (default 150), `--sims` (400) and `--lab-ticks`
(50000). `--minutes M` adds a wall-clock limit counted from the agent's first tool call;
after it only status, the block list and submit work. The agent then uses:

| Tool | Purpose |
|---|---|
| `./pd test design.json` | The dev test: verdict, reasons, volume, timings. Budgeted. |
| `./pd trace design.json` | Every block change, tick by tick, after placement and each flip (dust power included) |
| `./pd view design.json` | ASCII picture, one grid per z layer, with a legend |
| `./pd submit design.json` | Nominate the design to score; the last one counts |
| `./pd status`, `./pd blocks` | Budget and best-so-far; the allow-list |
| `./pd lab new\|flip\|step\|rest\|look\|view` | The lab: place any blocks, no door rules, and run them tick by tick |
| `./pd py` | Python in an interpreter that keeps its variables between calls, with the tools and the lab imported |

### The lab and the Python session

`test`, `trace` and `view` each need a complete, valid door and start from scratch every call.
The lab is the opposite: a world that keeps its state between calls. The agent places any
allow-listed blocks (any number of levers, no door rules), flips levers by position, advances
an exact number of ticks or until the build is at rest, and reads block states back. Its
budget is counted in game ticks advanced; starting a lab, flipping and looking are free.

- Every lab call rebuilds the lab world in the same simulator the tests use: it clears the
  area, places the lab's blocks, replays every flip and every tick run so far, then does the
  new operation. The simulator is deterministic, so the world is exactly where the last call
  left it, and nothing else that runs in between can disturb it. One lab world may run at most
  4000 ticks, which keeps a call under about a second.
- `./pd py` starts a small interpreter process in the kit folder on first use and sends it
  code over a localhost socket (address and a random token in `.pd_py`). It imports
  `pdbuild.Design` and everything in `pdlab.py`. The brief states its exact behaviour:
  output cap, timeout, what survives an error.
- The lab is on all three interfaces (the `pd` command, Python, Inspect tools). The Python
  session exists only in the command-line kit.

### Several runs at once

`python3 -m pdgrader serve-many spec.json` serves several runs from one process that shares
one simulator (about 450 MB). The spec is a JSON list of `{"name", "port", "n", "track",
"log", "kit", "variant", "minutes", "budget"}`. Jobs take turns on the simulator; each starts
from a cleared area, so runs cannot affect each other (a test checks this). `--resume`
restores every run from its log after a restart, and `--exclude START END` (unix seconds,
repeatable) keeps a window such as the machine being asleep from counting against any run.
The time limit itself runs on a monotonic clock, which stops while the machine sleeps.

`bench/` turns runs into results:

- `analyze.py <manifest> [--score]` writes `summary.json`: per run, the best volume after every
  test call against working minutes (excluded windows removed) and API-equivalent cost so far,
  token totals from the agent's transcript, and, with `--score`, the final test for finished runs.
- `export_dashboard.py <summaries...> --out <dir>` writes the `runs.json` and `curve.json` files
  the results page reads.
- `report_stats.py <wave folders...>` prints per task and model: runs, working doors, best and
  median volume, mean and spread of score, median minutes to the first door, mean cost and tests,
  and what the continue messages gained.

`../runs/bench/` holds the benchmark itself: one folder per wave (spec, manifest, logs, kits,
results), `reprompt.py` (the neutral continue message), `register.py`, `watchdog.py` (notifies
when a run passes its limit) and `FROZEN_BRIEF_NOTES.md` (facts held back from the frozen brief).

If the tool server dies mid-run (a crash, a reboot, the harness exiting), restart it with
`--resume` and the same `--n`, `--track`, `--port` and `--log`, and without `--kit`. Budgets,
time limit and variant come from the log. Calls used, lab ticks, the best design, the
submission and time used are restored, and the time with no server running is not counted.
The lab world is lost; the agent's files are not. The log gets a `resume` entry and the
score reports `server_restarts`.

When the run is over:

```bash
python3 -m pdgrader score runs/x/log.jsonl --out runs/x/result.json
```

This takes the last submitted design (or, with no submit, the smallest that passed `test`),
gives it the final test in a fresh simulator, and reports the verdict, volume, score against
the task's reference, the placement-robustness tag, and how the best volume improved test
by test. It also reports effort: test, trace/view and lab-tick counts, seconds from the first
tool call to the last (`seconds_active`) and to the first valid test (`seconds_to_first_valid`). For a run with no valid door it also reports `best_partial`: how far the best
attempt got (flips completed, plus the share of doorway cells that reached the target on the
flip that failed). That number is a diagnostic and never the score.

### As an Inspect task

`inspect_task/piston_door.py` wraps the same session as an Inspect AI task. The tools and the
scorer run in the Inspect host process, so the simulator and log stay outside any sandbox.

```bash
pip install -r inspect_task/requirements.txt
inspect eval inspect_task/piston_door.py --model <provider/model> -T sizes=2,3 -T tracks=seamless
```

`-T variants=scratch,improve` adds the shrink-a-given-door variant where a starting design exists.
`-T lab_ticks=N` and `-T minutes=M` set the lab budget and the wall-clock limit. The agent
gets the six lab tools (`pd_lab_new`, `pd_lab_flip`, `pd_lab_step`, `pd_lab_rest`,
`pd_lab_look`, `pd_lab_view`) but not the Python session.

`-T use_sandbox=true` adds bash and python in a Docker sandbox and lets the agent pass a
design file path. `inspect_task/smoke_mock.py` runs the whole task with a scripted mock
model and no API key.

### In a container

```bash
docker build -t pdgrader -f docker/Dockerfile .
docker run -d -p 127.0.0.1:8811:8811 -v pdlog:/var/pdgrader pdgrader \
    serve --n 3 --track seamless --port 8811 --host 0.0.0.0 --log /var/pdgrader/log.jsonl
```

The build fetches Mojang's server jar, so building means accepting the Minecraft EULA, and
the built image must not be published. Run one container per agent run and never mount the
log volume into the agent's container. Point the agent's `pd` at it with `PD_SERVER`.

## How it works

- `kernel/src/pd/PdKernel.java` starts Mojang's own headless test server, the class behind
  the vanilla `net.minecraft.gametest.Main` launcher, then takes over the server thread and
  advances the world one `ServerLevel.tick` at a time. No game code is patched and no mod
  loader is used. It places blocks, flips the lever, and after every tick records which
  cells changed, the doorway's state, the swept bounding box, entities, and whether any
  protected cell changed. It knows nothing about scoring.
- `pdgrader/validate.py` rejects malformed or disallowed submissions before simulation.
- `pdgrader/grade.py` builds the kernel job from the rulebook and turns the trace into a verdict.
- `pdgrader/rules.py` holds every rulebook constant, the geometry, and the block allow-list.
- `pdgrader/session.py` is one agent run: tools, the lab, budgets, log. `pdgrader/server.py`
  serves it over localhost HTTP and does final scoring. `pdgrader/kit.py` renders the task
  brief. `kit_template/` holds what the agent runs: `pd`, `pdbuild.py`, `pdlab.py`.
- `pdgrader/references.py` holds the reference volume per task and the starting designs for
  the improve variant. A reference is "verified" when this grader measured it on a design
  kept in `reference_designs/`; the rest are unverified community claims.

## What has been verified

- `python3 -m unittest discover -s tests`: 95 end-to-end tests pass. Nineteen (`test_kit2.py`) cover kit 2: one per
  added fact, the film against `trace` and against the lab's world, the `./pd film` command and the
  `Film` class through `./pd py`, and that kit 1 is unchanged. One more physics test covers the
  solvable changed-physics variant. Eight (`test_physics.py`) cover
  changed physics: each patch's measured effect in the lab against a vanilla simulator (repeater
  delay 2 to 3 ticks, observer 2/2 to 3/4 ticks and no block dropping, nine blocks pushed then
  refused), unknown settings, a run's physics matching its simulator's, logging, resume and
  scoring, the 3×3 reference failing under changed physics, and the brief. Two cover
  rectangular doors (2x1 and 1x2 hand-built doors in final mode and all 11 placements, the
  orientation check, a rectangular session with the lab, resume and brief). The other 65: Two of them check the shared
  simulator: two runs' labs and tests interleaved on one simulator give the same results as
  separate ones, and one lab world stops at 4,000 ticks. Eleven (`test_facts.py`)
  check component facts the brief states, in the lab: what holds dust, which blocks cut a
  diagonal dust step (every allowed block), the glass step, a listed cross being reshaped,
  that glass and observers do not conduct, quasi-connectivity and when a piston notices it,
  repeater inputs, comparator side input, observer pulses on a piston, and a piston pushed
  into a powered spot. Two cover resuming a run after a restart and that a stale
  Python-session file never stops an unrelated process. Fourteen cover the lab
  and the time limit, one per statement the brief makes about them: piston timing, step sizes
  adding up, nothing ticking between calls, the at-rest rule, placement, walls, the first
  entity, every refusal, the tick budget, and that tests and the lab do not disturb each
  other. One of them runs the 3×3 seamless reference door in the lab, once a tick at a time
  and once as rest, flip, rest, flip, rest, and checks every block change against what
  `trace` reports for the same door (same cell, same tick, same states). Eight run a real
  tool server and the `./pd` commands as separate processes: the lab commands, the Python
  session (variables kept across processes, errors, output cap, timeout, reset, idle exit,
  calls queued one after another), the Python tools and `Lab` class, and the worked example.
  The other 28 are as before. Nineteen cover three
  hand-built working doors (1×1 open, 1×1 seamless, 2×2 seamless) with exact expected volumes,
  eight static rejections, and seven simulation failures (starts powered, never settles,
  cannot reopen, item drop, pushes a wall block, too slow, not seamless), plus repeatability
  after messy jobs, final mode, scoring, partial progress, the placement check, the observer
  placement rule, and that every reference and starting door measures what the table says. Nine cover
  the agent session: budgets, free rejections, best tracking, submit rules, scoring from the
  log, dust changes in traces, and that every brief renders.
- Two pilot rounds (`../reports/Pilot findings.md`): six runs, then two 3×3 runs with the lab
  and the Python session, both of which produced valid doors (360 from scratch, 224 by
  shrinking the given door). Four verified reference doors
  came out of it, in `reference_designs/`: 2×2 seamless 30, 2×2 open 24, 3×3 seamless 192 and
  3×3 open 126. The two 3×3 doors were designed from scratch by agents within a run.
- `oracles/` holds a 3×3 door built separately as an existence proof (volume 1430, now the
  starting door for the improve variant) and a compacted version (420), with generator
  scripts and build notes. Both pass the final test and all 11 placements on both tracks.
- The Inspect task completes with a scripted mock model: tools respond (lab tools included,
  each ending with the time left), the final test runs, and the score is recorded. With
  `minutes` set, the task also sets Inspect's `time_limit` to that plus 10 minutes; that limit
  has never been reached in a run. It has not been run with a real model through Inspect, and the
  Docker sandbox option is untested.
- The container image builds, passes the same 63 tests on Linux, serves tool calls to a
  client outside the container, and shuts down cleanly on `docker stop`. Scoring a run from a
  container's log was checked on an earlier build.
- `tests/parity_dedicated.py` builds the same contraption on an ordinary dedicated server
  with console commands, steps it with `/tick step 1`, and compares every probed cell on
  every tick with the kernel's trace. Two contraptions match exactly over 16 ticks each: the
  2×2 door (31 cells) and an observer-driven sticky piston that drops and re-fetches its
  block on short pulses (5 cells). Both were rerun after the last kernel change.

## What has not

- Whether the lab helps agents is shown by one run's own account, not measured: no paired
  runs with and without it.
- The time limit refuses tools but cannot stop a command-line agent from thinking on; both
  round-2 agents ran about 85 minutes past it.
- The lab matching `trace` change for change is shown for one design (the 3×3 seamless
  reference), not proven in general.
- No community door has been graded, so the volume rule is not yet calibrated against a
  published record, and nothing with slime, honey or zero-ticks has been run.
- The pilot runs all predate the current brief and rules (v0.3). Benchmark waves cover 2×2,
  3×3, 4×4 and 3x2; see `../runs/bench/`.
- No 3×3 door is known to exist under all four physics changes; `observer_pulse=3` has not
  been measured. Comparators, torches and piston stroke time are not patchable.
- Parity with the dedicated server is shown for two small contraptions, not proven in general.
- Timings are from one Apple M4 laptop: about 50 ms per dev grading natively, about 100 ms
  in a Linux container on the same machine (arm64, Docker Desktop). x86 Linux is untested.
- Containers (hoppers, droppers) and partial blocks are not implemented. Robustness covers
  shifts and half turns only.
- The component facts in the brief that predate round 2 were checked by hand with small
  probes and are not in the test suite; the ones added after round 2 are.
- The final-mode parameters are in `rules.py`; an agent with read access to this folder can see them.

## Things that bit during the build

- A chunk does not tick its block entities, moving pistons included, until its entity
  storage has loaded, which completes as a task on the server thread. The kernel hands the
  thread back while it waits; without that, pistons in freshly loaded chunks froze mid-move.
- 26.3 structure files use `id`/`properties` in the palette. The older `Name`/`Properties`
  form loads without error and places air.
- `/setblock` runs a shape update on the block it places, which makes an observer fire. The
  grader's placement skips that for observers, so the dedicated-server comparison asks the
  kernel for the older behaviour (`legacy_placement`).
- A piston ignores power arriving at the face it pushes from.
- A lever on the side of a piston drops as an item the moment that piston extends (an
  extended piston's base has no full side face). It shows up in the lab as `ENTITY appeared`.
