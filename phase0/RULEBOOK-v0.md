# Piston door eval: rulebook v0.3 (draft, not frozen)

This is the document the grader in `grader/` implements. Every rule is written so that a
program can check it. Rules marked **[proposed]** were my defaults; you accepted them all on
2026-11-09, so they now stand unless you change one. Rules marked **[confirm with Squid]**
follow my reading of the community ruleset (Squid Records) and should still be checked with
its maintainers before freezing.

Changes from v0 (made while building the grader) and from v0.1 (made after the pilot) are
listed at the end.

## Decisions (all accepted 2026-11-09)

| # | Decision | Default in force | What it changes |
|---|---|---|---|
| 1 | Time cap per open or close | 200 game ticks (10 s), including coming to rest | Selects the human reference at each size. 100 ticks still admits the 3×3–5×5 references found; the 484-block 7×7 needs about 660. |
| 2 | Input device | One lever, starting off; the submission says whether that is open or closed | A button needs a toggle circuit inside the door, which adds volume and difficulty. Community records allow either. |
| 3 | Door and wall material | `minecraft:stone` for both | Makes "closed door looks like wall" a plain block-equality check. |
| 4 | Headline position rule | One fixed position; pass-rate at shifted positions reported as a tag | The alternative (must pass everywhere) excludes locational designs, which the community allows. |
| 5 | Size excludes the lever | Yes, as in Squid | Keeps volumes comparable with human records. |
| 6 | Game version | Java 26.3 | Latest release; some older record doors may not work on it and must be re-verified. |
| 7 | The build must come to rest | Yes: no block may change for 20 ticks | Bans free-running clocks, which community records allow. Without it "finished opening" has no clean definition. |

## 1. Platform

- Minecraft Java Edition 26.3, vanilla server jar (SHA-1 `33680f5f2ac32864d6d7cf5e56a705fdb3e05f4c`), Java 25.
- Feature flags: `vanilla` plus `trade_rebalance`, which is what Mojang's own test server enables. Redstone Experiments and Minecart Improvements are off.
- Overworld, empty space around the build, no players.
- The doorway's local (0, 0, 0) is world position (0, 100, 0). That puts the doorway on a chunk border in x and z. **[proposed]**
- The benchmark never redistributes the server jar; the harness downloads it and the operator accepts Mojang's EULA.

## 2. Coordinate frame and task

A task is "N×N door" for N in {2, 3, 4, 5, 6, 7}, in a track (section 6).

- **Doorway cells** D: (x, y, 0) for 0 ≤ x < N and 0 ≤ y < N.
- **Hallway cells** H: (x, y, z) for the same x, y and every z ≠ 0. The hallway must be air at every tick.
- **Wall cells**: every cell with z ≠ 0 that shares a face with a hallway cell. The harness fills them with the wall block out to the edge of the test volume, and they must hold that block at every tick.
- **Frame cells**: the cells at z = 0 that share a face with a doorway cell. They belong to the submission.
- **Closed** means every cell of D holds the door block. **Open** means every cell of D is air.
- The test volume is 48 × 48 × 48 around the doorway. No block may leave it.

## 3. Submission format

`{"initial_state": "open" | "closed", "blocks": [{"pos": [x, y, z], "id": "...", "props": {...}}]}`

- Exactly one `minecraft:lever`, with `powered` false. **[proposed]**
- Every block id, property and value must be on the allow-list (section 7). Anything else is rejected before simulation, with the position and the allowed values.
- No block in a hallway cell or a wall cell. Doorway cells may hold only the door block and must match `initial_state`.
- An extended piston must have its matching piston head, and a piston head its extended piston.
- Properties that the game derives, such as dust power and dust shape, may be left out.

## 4. Test procedure

1. **Validate** the submission. A failure here never reaches the simulator.
2. **Place and settle.** All blocks are placed silently, then every block gets one shape update and one neighbour update in (x, y, z) order, like pasting a schematic and then updating it. The build must stop changing within 40 ticks, and the doorway must then match `initial_state`. Blocks that did not survive placement are reported as a warning. Observers are skipped in the shape update, so an observer does not fire merely for being placed (matching a hand-placed observer in Java Edition). Other side effects of the update play out during settling, for example anything a lit torch powers moves. A submission describes the build before settling, and `initial_state` describes it after.
3. **Cycle** 3 times in the agent-facing test, 8 times in the final test. For each flip of the lever:
   - within the time cap the doorway must reach the opposite state and stay there, and the whole build must be at rest: no block changes for 20 consecutive ticks;
   - it must then hold unchanged for a further 40 ticks.
4. **Whole-run rules**, checked every tick: no entity anywhere in the test volume (item drops and falling blocks count), every wall cell intact, every hallway cell empty, nothing outside the test volume.
5. **Final test extras**: a fresh simulator process per submission, and extra idle ticks before each flip (0, 1, 2, 3, 5, 7, 11, 13 ticks and so on) so that flips land on different game-time phases. A flip is never issued before the build is at rest, so doors need not be spam-proof.

All tick counts are exact.

## 5. Size

- **Volume** is width × height × depth of the smallest axis-aligned box containing every cell that held a submission block at any tick, from placement through every cycle, together with the doorway cells. **[confirm with Squid]**
- Excluded from the box: the lever, and the harness's wall blocks.
- Door blocks count wherever they are, so blocks stored inside the mechanism while the door is open are inside the box.
- Reported alongside, never mixed into the score: block count at rest (lever and wall blocks excluded), opening time, closing time, and reset time, all in game ticks. Opening or closing time is the tick from which the doorway stays in its new state; reset time is the last tick on which any block changed.
- Still to do: rebuild a published record door and confirm the grader reproduces its published volume (for example the 56-block 3×3 as 7 × 8 × 1).

## 6. Tracks

| Track | Visibility rule |
|---|---|
| Open | None. Any working door. This is the easy rung and has no community records. |
| Seamless | At every rest state, each cell beside an empty doorway cell must hold a plain block (section 7). With the hallway walls intact, nothing but plain blocks and air can then be seen from inside the hallway. |

- When the door is closed the doorway is full of door blocks, so nothing behind it is visible and the rule has nothing to check. In practice the rule constrains the frame cells while the door is open.
- Transitions are not checked for visibility (that would be the community's "super seamless").
- Door block and wall block are the same material, so a closed door is indistinguishable from a wall across the hallway. **[proposed]**
- The exact community tier table was not readable during research. **[confirm with Squid]**

## 7. Block allow-list

- **Plain blocks:** stone, smooth stone, iron block and the sixteen concrete colours. Full, opaque, movable cubes with no behaviour beyond conducting power.
- **Components:** piston, sticky piston, piston head (only as part of an extended piston), redstone dust, repeater, comparator, redstone torch and wall torch, redstone block, observer, slime block, honey block, target block, note block, lever, obsidian, glass, white glazed terracotta.
- **Deferred to v1:** hoppers, droppers and dispensers (they need a rule for initial contents and can create item entities); slabs, trapdoors, walls and other partial blocks that compact doors use.
- **Banned:** everything else, including command blocks, structure blocks, `moving_piston` placed directly, fluids, gravity blocks, TNT, rails and anything that creates or needs an entity.
- Allowed by default, as in the community rules: quasi-connectivity, zero-tick pulses and update-order effects. They are vanilla behaviour on the pinned version.

## 8. Verdict and score

- A submission is **valid** only if it passes validation and every check above.
- Score per task: 0 if invalid, otherwise reference volume ÷ submission volume, uncapped.
- The reference per task and track is frozen in a table with source, date and the volume the benchmark's own grader measured for it. No reference is used until the grader has re-verified it under these rules. This table does not exist yet.
- Position robustness is reported as a tag: the number of 11 other placements at which the same submission is still valid. Eight are shifts (odd and even offsets on each axis, and offsets that cross chunk and chunk-section borders); three are the build turned half a turn about the doorway's vertical axis, at the pinned position and two shifts. It does not change the score. Quarter turns are not covered: they would turn the hallway and so change the task. **[proposed]**
- **Partial progress** is reported for invalid submissions as a diagnostic, never as score: (lever flips completed + share of doorway cells that reached the target on the flip that failed) ÷ flips in the test. A door that never moves gets 0.

## 8a. A run

- One agent run gets one task, a budget of test calls and a budget of trace/view calls (pilot: 120 and 300). Submissions rejected in validation are free.
- The agent also has a lab: a separate world where it can place any allow-listed blocks, with none of the door rules, and run them tick by tick. Nothing in the lab is scored and it cannot affect a test. Its budget is counted in game ticks advanced (default 50,000).
- A run may have a wall-clock limit, counted from the agent's first tool call. After it, testing and the lab are refused; submitting still works. No limit is set by default.
- The agent sees only the dev test (3 cycles). The final test parameters are applied once, after the run.
- The scored design is the last one the agent submitted; with no submission, the smallest design that passed a dev test.
- Reported per run: verdict, volume, score, robustness tag, calls and lab ticks used, time from the first tool call to the first valid test and to the last call, the best-volume-so-far curve over test calls, and best partial progress.

## 9. Open items

- Confirm sections 5 and 6 with the Squid maintainers, and get the current record list (their API hostname was not found).
- Obtain and re-verify community doors; none has been run through the grader.
- The container rule; partial blocks.
- A reference door for every size and track, measured by this grader. So far: 2×2 seamless 30, 2×2 open 24, 3×3 seamless 192, 3×3 open 126, all from the pilot (the community claims 56 for 3×3). Nothing for 4×4 and up.
- Choose where the final-test parameters live so the agent's sandbox cannot read them. They are in the grader's source today.
- Legal check of the EULA position for a published harness.

## Changes from v0

- **Lever polarity is free.** v0 said lever-on must mean open, which forced an inverter into every simple door.
- **Placement is paste-then-update**, and the build may adjust itself while settling. v0 said nothing may move after placement, which would have made agents hand-specify dust power levels.
- **Seamless is stated as visibility**: cells beside an empty doorway cell must be plain. v0 required every frame cell to be plain in both states, which wrongly rejected a piston head hidden behind a closed door.
- **Rest is required** (decision 7), so free-running clocks fail.
- **Hallway and wall cells are checked every tick**; v0 only said the hallway "must be air".
- **Final-test extras** dropped the repeater-timed input, which has no meaning for a lever.

## Changes from v0.1 (after the pilot)

- **Robustness tag covers 11 placements**, adding three half-turn placements to the eight shifts.
- **Placement side effects are stated** (section 4, step 2).
- **Partial progress** is reported for failed doors, because 3×3 attempts otherwise all score the same zero.
- **A run is defined** (section 8a): budgets, which design is scored, and what is reported.

## Changes from v0.2

- **Observers no longer fire on placement.** Under v0.2 every observer pulsed once when the design appeared, an artifact of the placement update. It surprised a pilot agent and was the one real obstacle in building the 3×3 reference door, which needed a pre-powered repeater just to swallow the pulse. Run logs record the rules version; logs from before this change are scored under the v0.2 placement rule.
- **3×3 has verified references** (192 seamless, 126 open, both designed from scratch by pilot agents) and a starting door for the improve variant (volume 1430).
