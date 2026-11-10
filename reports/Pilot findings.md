# Piston door eval: pilot findings (2026-11-09)

Six agent runs, all finished and scored. One run per cell, so read this as a smoke test of
the eval and a first look at difficulty, not a measurement of the models.

## What was run

Each run was one agent with a working folder (the task brief, the `pd` client, an example),
120 test calls and 300 trace/view calls, talking to its own tool server. The agents were
subagents of this session, not runs through Inspect, so effort and stopping behaviour are
whatever the subagent harness gives.

| Run | Model | Task | Started from | Final verdict | Volume | Tests used | Trace/view used | Wall time |
|---|---|---|---|---|---|---|---|---|
| a | Fable | 2×2 seamless | A working 110-volume door | Valid | 30 (6×5×1) | 1 | 1 | 10 min |
| d | Sonnet | 2×2 seamless | A working 110-volume door | Valid | 30 (6×5×1) | 1 | 0 | 6 min |
| e | Haiku | 2×2 seamless | A working 110-volume door | Valid | 60 (6×5×2) | 3 | 9 | 10 min |
| f | Sonnet | 3×3 open | Nothing | No valid door | – | 1 | 2 | 71 min |
| b | Fable | 3×3 open | Nothing | Valid | 126 (7×9×2) | 2 | 15 | 155 min |
| c | Fable | 3×3 seamless | Nothing | Valid | 192 (8×8×3) | 4 | 18 | 166 min |

- "Valid" means the door passed the eight-cycle final test in a fresh simulator.
- Every valid door passed all 11 shifted and turned placements except run b, which passed 8
  (see finding 5).
- Runs a and d used the first version of the brief. Runs e, f, b and c used a revision made
  after a and d reported. None used the brief as it stands now.

## Findings

**1. The 2×2 task is saturated.** Fable and Sonnet each wrote a 30-volume door and passed on
their first test; the designs differ only in where the lever sits. Haiku needed three tests
and stopped at double the volume. So 2×2 separates a small model from a large one but not
frontier models from each other. Keep it as the tutorial rung and a harness regression check.

**2. The 3×3 task is where models separate.** Fable built a valid door from nothing on both
tracks, and each first test passed. Sonnet built none. The reason 3×3 is hard is one cell:
eight doorway cells need one piston pushing one block one step, but the centre needs a block
to travel two steps through a cell that must itself end up filled. That forces a timed
sequence of short pulses, and a different sequence to undo it. Sonnet identified this
correctly, judged the build too large to debug, and stopped after one test.

The Sonnet result needs a rerun before it means much: its brief let it read the hallway
walls as filling everything off the door's plane, so it treated the task as two-dimensional.

**3. Volume responds to effort, and there is a lot of headroom.** Run c went 840 → 320 → 256
→ 192 over four tests; run b went 315 → 126 over two. The best community claim for an
entity-free 3×3 is 56 (not rebuilt in this grader, and made under looser rules), so the best
pilot doors are roughly two to three times that. The metric has room to move in both
directions.

**4. Agents barely used the tools.** Across all six runs they used 12 of 720 test calls and
45 of 1,800 trace/view calls. The 3×3 runs spent about two and a half hours each, nearly all
of it reasoning between a handful of calls. Both Fable 3×3 agents said they stopped because
they ran out of ideas, not budget. Two consequences:
- The call budget is not the binding constraint. Wall time and tokens are. The three 3×3 runs
  used roughly 210k, 435k and 480k tokens.
- A real harness should set the stopping rule itself (for example, refuse "finish" while the
  door is invalid and budget remains, or run a fixed number of improvement rounds). That is
  not built.

**5. The robustness tag caught a real fragility.** Run b's door failed all three half-turn
placements while passing every shift. The cause was tied to finding 6: with observers no
longer firing on placement, the same door passes all 11.

**6. One harness artifact hurt every 3×3 builder, and is now removed.** The grader pastes a
design in and then updates every block. That update made every observer fire once, which
real hand-placed observers in Java Edition do not do. All three 3×3 builders (both Fable
runs and the reference-door build) had to work around it, typically with a pre-powered
repeater whose only job was to swallow the pulse. Under rulebook v0.3 observers no longer
fire on placement. Run logs record the rules version, and the pilot runs are scored under
the rule they ran with.

**7. The seamless rule costs volume, as intended.** On 2×2, removing the two floor frame
blocks from the 30-volume door gives a 24-volume door that passes the open track and fails
seamless. On 3×3 the open door is 126 and the seamless door 192, though those are different
designs from different runs.

**8. Dev and final verdicts agreed.** All five doors that passed the three-cycle dev test
also passed the eight-cycle final test. Run c's agent noted its door has only two ticks of
timing margin, and it still passed at every flip timing the final test uses.

## Reference volumes after the pilot

| Task | Volume | Source |
|---|---|---|
| 2×2 seamless | 30 | Pilot runs a and d |
| 2×2 open | 24 | The 30 door with its floor frame blocks removed |
| 3×3 seamless | 192 | Pilot run c |
| 3×3 open | 126 | Pilot run b |
| 4×4 and up | none measured | Community claims only (132 for 4×4, 504 for 5×5), unverified |

- All four measured references are files in `grader/reference_designs/`, and a test checks
  that the grader still measures each at the volume in the table.
- Run c's door was made under the old placement rule. Its one pre-powered repeater is
  un-powered in the stored file; with that single change it passes the current rules and all
  11 placements.
- A reference is the best door this grader has seen, not a proven minimum. A score above 1
  means it was beaten.

Separately, I had a 3×3 door built outside the pilot to prove the task solvable under these
exact rules. It works (volume 1430, compacted once to 420) and is now the starting door for
the "shrink a given door" variant. Both pilot doors turned out much smaller.

## Where the time went (added 2026-11-10)

Read from each run's server log. Times are minutes since the tool server started, which was
moments before the agent did.

| Run | First tool call | First valid door | Improvements after that | Last call |
|---|---|---|---|---|
| a, Fable 2×2 | 10 | 10 (volume 30) | none | 10 |
| d, Sonnet 2×2 | 6 | 6 (30) | none | 6 |
| e, Haiku 2×2 | 6 | 8 (70) | 60 at minute 9 | 10 |
| f, Sonnet 3×3 open | 46 | never | – | 71 |
| b, Fable 3×3 open | 84 | 144 (315) | 126 at minute 153 | 155 |
| c, Fable 3×3 seamless | 34 | 123 (840) | 320 at 137, 256 at 142, 192 at 166 | 166 |

- **Getting the first working 3×3 door took about two hours; shrinking it took minutes.** Run
  b cut its volume by 60% in 9 minutes. Run c cut it by 77% in 43 minutes, three steps of 5
  to 24 minutes each.
- **Much of the two hours passed with little or no tool use.** Run b made no tool call for 84
  minutes; run c made three in its first 114. Each Fable run's first `test` call was a
  complete door that passed. Every tool required a whole design that met the format rules
  (exactly one lever, correct doorway contents), so there was no way to try a part by itself.

Two changes followed from this:

- **A lab**: an empty world where an agent places any part, flips levers and steps tick by
  tick, with no door rules, plus a Python session that keeps its variables between calls.
- **An optional time limit** per run, counted from the first tool call.

## Round 2: two 3×3 runs with the lab (2026-11-10)

Both runs used Fable on 3×3 seamless, the current brief and rules, the lab and the Python
session, and a 90-minute limit. Run g started from nothing. Run h was handed the working
1430-volume door to shrink (the "improve" variant).

| Run | First working door | Best door | Final test | Placements | Tests used | Lab |
|---|---|---|---|---|---|---|
| g, from scratch | minute 27, volume 360 | 360 (9×8×5) | valid | 11/11 | 2 | 2 worlds, 454 ticks |
| h, shrink the 1430 door | minute 29, volume 280 | 224 (7×8×4) | valid | 11/11 | 6 | not used |

Minutes are counted from the agent's first tool call. The verified reference is 192, so the
scores are 0.53 and 0.86. Neither run beat round 1's best.

- **Time to a first working door fell from about two hours to under half an hour.** Round
  1's seamless run (c) needed 123 minutes; run g needed 27, and its first test passed. Run g
  credits the lab: two short experiments settled the mechanism and a timing race before it
  wired anything. This is one run, and the brief and rules also improved between rounds, so
  the lab's share of the gain is not measured.
- **Run h did not use the lab.** Its first test was a nearly complete door, and test plus
  trace fixed it in three rounds. It said afterwards that the lab would have been the right
  tool for the three component behaviours it learned through failed tests.
- **Shrinking stalled where layout, not mechanism, was the problem.** Run g's attempt at 320
  failed to close: moving dust next to a dust cross connected to it diagonally and turned
  the cross into a line. Run h found no 3-layer layout (168) because two signal lines needed
  the same cells.
- **Both agents kept thinking long after their time ran out.** The limit makes the tools
  refuse work, but nothing stops the agent: g stopped at 172 minutes and h at 176, with no
  tool call after minute 62. A harness has to end the run itself. The Inspect task now does
  (the sample ends 10 minutes after the tool limit). This has not been run with a real model.
- **Both agents misjudged the clock.** Thinking between calls counts, and one stretch with
  no calls took h from minute 38 to 59. Every tool reply now ends with the time left.
- **An API timeout cut both runs off** at minutes 27 and 30. A restarted tool server can now
  restore a run from its log (budgets, best design, submission, time used), and both agents
  were resumed. The scores above include the time after the restart.

### What the agents said the brief was missing

Each claim was checked in the lab before anything was added.

| Claim | Checked | In the brief now |
|---|---|---|
| A listed dust cross is lost when dust one step up or down connects to it | True | Yes |
| Which blocks cut a diagonal dust step is not stated | Every allowed block tested | Yes: glass, honey, observers, pistons and redstone blocks do not cut it |
| A comparator reads side input from dust beside it | True | Yes |
| Dust can sit on a piston | True (facing north, up, down) | Yes |
| Dust on glass passes no power down one step | True | Yes |
| An observer conducts power like a solid block | **False**: a piston beside it does not move | States that it does not |
| Quasi-connectivity counts power from above the cell over a piston | True, but the piston only reacts when something next to it changes | Yes, with the update rule |
| A repeater reads an observer's output and a lever-powered block | True | Yes |
| An observer on a piston fires once per extend and once per retract | True | Yes |
| A piston pushed into a powered spot starts one tick after it lands | True | Yes |
| The time limit includes thinking time | True | Yes, plus time left on every reply |

Each of these is now a test (`grader/tests/test_facts.py`), so a game or kernel change that
breaks one fails the suite.

## What the agents said was unclear, and what changed

| Reported by | Problem | Change |
|---|---|---|
| 2×2 agents | Unclear whether frame blocks and the lever count toward volume | Brief states both rules |
| 2×2 agents | Unclear whether hallway and wall checks apply mid-motion | Brief says every tick, including while parts move |
| Haiku | `trace` did not show redstone dust changing power | Fixed |
| Haiku | Dust rules not stated | Brief states what dust connects to and powers; each claim checked in the simulator |
| Sonnet 3×3 | Read the walls as filling everything off the door's plane | Brief gives the wall tube by coordinates and says wiring can run in three dimensions |
| All 3×3 builders | Observers fire once at placement | Removed in rulebook v0.3 |
| Sonnet 3×3 | No piston or repeater timings | Brief lists measured timings |
| Both Fable 3×3 | A lone dust is a dot that powers nothing sideways; the brief said to leave shape out | Brief says listing all four sides makes a cross |
| Fable 3×3 open | The "changed on placement" warning reads like an error | Reworded as a note that is not a failure |
| Fable 3×3 seamless | Glass and observers hold dust; glass ladders only carry a signal upward | In the brief |
| Fable 3×3 seamless | Trace's doorway summary line and `--limit 0` were undocumented | Documented in the brief |
| Reference builder | Quasi-connectivity named but not explained | Brief explains it and when to check for it |

## Other changes made because of the pilot

- **Partial progress** is reported for failed doors: flips completed, plus the share of
  doorway cells that reached the target on the flip that failed. It is a diagnostic, never
  the score.
- **Two task variants:** `scratch` (design from nothing) and `improve` (shrink a working but
  bulky door). Starting doors exist for 2×2 and 3×3.
- **Rule versioning:** every run log records the rulebook version it ran under.
- The rulebook is at v0.3.

## What this means for the eval design

- **3×3 is the right centre of gravity today.** One frontier model solves it and one did
  not, volume moves with effort, and the best doors are well short of human records.
- **The size ladder is a depth ladder.** Difficulty goes with how deep the deepest doorway
  cell is: 2×2 is depth one, 3×3 and 4×4 depth two, 5×5 and 6×6 depth three, 7×7 depth four.
  4×4 is the natural next test: four cells each need the 3×3 centre trick. Nothing above 3×3
  has been attempted or shown solvable in this grader.
- **Cost per run is the practical limit.** A 3×3 attempt took about two and a half hours and
  several hundred thousand tokens. Larger doors will cost more, so run counts will be small
  and variance matters.

## Not yet known

- Run-to-run variance. Every cell above is a single run.
- How Sonnet does on 3×3 with the current brief.
- How much of round 2's speed-up comes from the lab and how much from the better brief. That
  needs paired runs with and without the lab.
- Whether anything above 3×3 is solvable within a run.
- How the grader's volume compares with community measurements. No community door has been
  rebuilt in it.
- Behaviour through Inspect with a real model. The Inspect task has only been run with a
  scripted mock.
