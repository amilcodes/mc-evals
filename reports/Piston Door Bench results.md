# Piston Door Bench: first results (2026-11-13)

Four Claude models each built working Minecraft piston doors, as small as they could, in
24 timed agent runs. Door size works as a difficulty ladder. The 3×3 door splits the models
into three clear tiers: Haiku 5.5 never built one, Sonnet 5.5 built large ones, and Fable 5.2
and Opus 5.5 built small ones. The 4×4 door then separates Fable from Opus by a factor of
ten. The best doors are far below any known limit, so the eval has a lot of headroom.

Results page: Piston Door Bench (claude.ai artifact). Every number below comes from the run
logs and agent transcripts in `runs/bench/`, and every door was re-tested in a fresh
simulator before it counted.

## What one run is

- **Task.** Build a seamless N×N piston door for Minecraft Java 26.3 that a grader runs in
  the real game engine: one lever opens and closes it, eight cycles at varied timing, nothing
  may enter the hallway, no item drops. **Score = reference volume ÷ the door's bounding-box
  volume**, so smaller is better and 1 matches the reference. No working door scores 0.
- **References.** 3×3: 192, the best door the grader had seen before this benchmark. 2×2: 30.
  4×4: 132, a community claim never rebuilt in this grader.
- **Tools.** Test (full verdict), trace (tick-by-tick block changes), view (ASCII layers), a
  lab (place any blocks, flip levers, step ticks), and a Python session that keeps state.
  Budgets were generous (150 tests, 400 traces, 50,000 lab ticks) and never the limit.
- **Time.** 120 minutes for 3×3, 150 for 4×4, 60 for 2×2, counted from the first tool call.
- **The loop.** An agent that stopped with time left got the same neutral message: its best
  volume so far, the time left, and "keep working". At most three times per run.
- **Fixed conditions.** The task brief was frozen for the whole benchmark; facts the agents
  found missing were logged, not added. All runs used the same harness, one shared simulator,
  and the same prompt.

## Results

### 3×3 seamless (four runs per model)

| Model | Working doors | Best volume | Median volume | Mean score | Score spread (sd) | First door (median minutes) | Mean cost per run |
|---|---|---|---|---|---|---|---|
| Fable 5.2 | 4 of 4 | **70** (7×10×1) | 164.5 | **1.50** | 0.86 | 34.6 | $41.14 |
| Opus 5.5 | 4 of 4 | 80 (8×10×1) | 185 | 1.29 | 0.79 | 67.1 | $22.82 |
| Sonnet 5.5 | 4 of 4 | 405 | 570 | 0.31 | 0.20 | 53.4 | $10.00 |
| Haiku 5.5 | 0 of 4 | – | – | 0 | 0 | – | $1.04 |

- Volumes per run. Fable: 70, 140, 189, 224. Opus: 80, 154, 216, 312. Sonnet: 405, 420, 720, 3375.
- Costs are what the same tokens cost at Claude API list prices, read from each transcript.

### The size ladder

| Model | 2×2 (60 min) | 3×3 (120 min) | 4×4 (150 min) |
|---|---|---|---|
| Fable 5.2 | not run | 4 of 4, best 70 | 2 of 2, best **264** (score 0.50) |
| Opus 5.5 | not run | 4 of 4, best 80 | 2 of 2, best 2,574 (score 0.05) |
| Sonnet 5.5 | 1 of 1, 30 | 4 of 4, best 405 | 0 of 1 |
| Haiku 5.5 | 2 of 2, 30 and 60 | 0 of 4 | not run |

Each rung separates a pair of neighbours: 2×2 shows Haiku can build a door at all, 3×3
separates Haiku (none) from Sonnet and Sonnet from Opus and Fable, and 4×4 separates Sonnet
(no door) from Opus (working doors, ten to twenty times larger) from Fable.

## Findings

**1. Three tiers on 3×3, and 4×4 splits the top tier.** On 3×3 every Sonnet door is larger
than every Opus door, and Haiku built none, so those separations hold run by run. Fable and
Opus overlap: Fable's doors were 70, 140, 189 and 224, Opus's 80, 154, 216 and 312, mean
scores 1.50 and 1.29 with spreads near 0.8. Four runs each cannot tell them apart on score.
What does separate them is speed and the bigger door: Fable reached its first working 3×3
door in a median 35 minutes against Opus's 67, and on 4×4 Fable's doors (264, 400) were
about ten times smaller than Opus's (2,574, 5,236).

**2. The task is far from saturated.** Fable's best 3×3 door is 70, a single-layer design
that scores 2.74 against the old reference; the best community claim for this door is 56,
made under looser rules. On 4×4, Fable's best is 264, twice the community's unverified
132-volume claim, and Opus's best is ten times larger again. Nothing here is near a ceiling.

**3. Telling an agent to keep going pays off, but it refines rather than rescues.** Of the
19 runs that had a working door when first told to continue, 10 then made it smaller: 112 → 70,
231 → 154, 252 → 189, 88 → 80, 4,320 → 2,574, 360 → 312, 504 → 405, 5,940 → 5,236, 154 → 140
and 765 → 720. Measured on a log scale from first working door to final door, about a quarter
of the improvement came after the first continue message. No run that had no door when told
to continue built one afterwards.

**4. Haiku's failure is consistent and specific.** In all four 3×3 runs Haiku never called
`test`. It wrote search models in Python, concluded the mechanism was too hard to wire, and
stopped, often within 20 minutes. On 2×2, where one piston per cell suffices, it built
working doors within 10 minutes.

**5. Cost tracks capability, except that Opus is the best value.** On 3×3 Fable cost $41 a
run, Opus $23, Sonnet $10 and Haiku $1. Per point of score, Opus is cheapest at about $18,
then Fable at $27 and Sonnet at $32.

**6. Doors that pass the test are not always robust.** The robustness check rebuilds every
door at 11 other positions and orientations. All 12 Fable and Opus doors passed all 11. Two
Sonnet 3×3 doors passed 7 and 8, and one Haiku 2×2 door passed 6: they work where they were
built and fail elsewhere. The score does not penalise this; the results page shows it.

## What happened along the way

- **The laptop slept for six hours** (03:25 to 09:21), with eight runs in progress. The time
  limit then used wall-clock time, so the sleep counted against them and one 4×4 run was
  refused with "time is up" after about 50 minutes of real work. The servers were restarted
  with that window excluded, that agent was told what happened, and the time limit now runs
  on a clock that stops while the machine sleeps. No agent was lost; all resumed on waking.
- **Stopped by the harness:** one Haiku 3×3 run that went idle on a background job, and one
  Sonnet run that thought past its time limit.
- **Rule breaches:** one Haiku agent created and deleted an empty file in `/tmp`; one Sonnet
  agent tried to write a script there and was blocked. Neither touched the grader.
- **An edge case worth a rule decision:** Fable's 70 door hangs its lever just off the door's
  plane. The rules do not count the lever's cell, so this is legal, and it is what makes a
  single-layer door that narrow.
- **Brief gaps the agents found** (dust on sideways pistons pops, note blocks as edge
  detectors, the exact build region, and about 25 others) are in
  `runs/bench/FROZEN_BRIEF_NOTES.md`. Adding them is a new brief version and needs fresh
  baselines.

## How much it cost

24 runs, about 29 agent-hours and $460 at API list prices: Fable $247, Opus $160, Sonnet $49,
Haiku $5. Each model had six runs.

## What a stronger version needs

- **More runs per cell.** Four runs per model on 3×3 settle the tiers but not the order of
  Fable and Opus: their spread within a model (about 0.8) is four times the gap between them
  (0.21), so 3×3 score alone would need far more runs than this budget allowed. 4×4 showed a
  tenfold gap with two runs each, which makes it the better rung for the top models.
- **The harness must end runs.** Time limits refuse tools but do not stop an agent from
  thinking; one run here went past its limit and had to be stopped by hand.
- **4×4 as the main rung for frontier models**, with 3×3 as the entry rung. 4×4 separates
  Fable from Opus by a factor of ten and has a known target well below Fable's best.
- **Reproducible model access.** These runs used subagents of a coding assistant. The Inspect
  task in `grader/inspect_task/` runs the same tools against the API; it has only been tested
  with a scripted model.
- **The next brief version**, with the held-back facts added, then re-baselined.
