# Single-edit census, 16 Nov 2026

The census graded every design exactly one block edit away from two seed doors.

**Seeds**
- Fable's 70-volume 3×3 (`w1-fable-a`)
- Opus's 240-volume 4×4 (`w4-4x4-opus-e`)

**The edits**
- **Cells:** every cell of the seed's bounding box, except the doorway, the hallway, the hallway walls and the lever.
- **States:** each cell was set to each of 57 block states:
  - air, which deletes the block
  - the plain and special blocks
  - pistons and sticky pistons in 6 facings
  - observers in 6 facings
  - repeaters in 4 facings × 4 delays
  - comparators in 2 modes
  - wire, torches and wall torches

**Grading**
- Every neighbour got the dev grade: 3 cycles, seamless track, vanilla 26.3.
- Every neighbour that passed got the final grade: 8 cycles with offset flips.

Script: `census.py`. Raw results: `census_<run>.jsonl`. Summaries: `analysis_*.json`.

## Results

| | Fable 70 (3×3) | Opus 240 (4×4) |
|---|---|---|
| Neighbours graded | 3,416 | 8,960 |
| Wall-clock time (4 simulators) | 344 s | 960 s |
| Still valid (final grade) | 815 (23.9%) | 2,288 (25.5%) |
| …of which: filling an empty cell | 730 of 784 (93%) | 2,056 of 2,352 (87%) |
| …of which: changing an existing block | 85 of 2,632 (3.2%) | 232 of 6,608 (3.5%) |
| Deleting any single block | 0 of 47 work | 0 of 118 work |
| Existing blocks with no working alternative | 33 of 47 (70%) | 76 of 118 (64%) |
| Smaller door found | none | none |
| Faster door at the same volume | 3, all at one cell | none |
| Passed dev but failed final | 0 | 0 |
| Broken neighbours failing on the very first flip | 2,385 of 2,601 (92%) | 6,035 of 6,672 (90%) |

## What it says

1. **Both doors are irreducible under single edits.**
   - Removing any one block breaks the door, so no single edit can shrink either door.
   - Most working edits are neutral: they fill empty space or swap filler stone for other solid blocks.
   - The mechanism itself is almost rigid. About two thirds of the existing blocks have no working substitute.
2. **Speed is locally improvable on the Fable door.**
   - Replacing the delay-4 repeater at (2, 5, 0) with a west-facing observer gives a door that opens in **28** ticks instead of 34 and closes in **16** instead of 22, at the same volume of 70.
   - It passes the final grade, all 11 placement shifts and the 180° turn (`robust_fable70.json`; design in `fable70_observer.json`).
   - That beats the best repeater-delay setting, which reaches 30 and 18.
3. **The Opus 240 is a local optimum for both size and speed.** Every working re-timing was the same speed or slower: 52/40 up to 60/48.
4. **The dev grade predicted the final grade perfectly:** 0 disagreements in 12,376 designs. So screening with the cheap grade and confirming only survivors is safe.
5. **The grader's built-in partial score gives almost no gradient.**
   - About 90% of broken neighbours score 0 flips passed, and there are only 15–21 distinct partial values.
   - A STOKE-style "almost works" search would need a finer score than this. For example, compare per-tick doorway states or piston event timing against the seed.

## Decision, following the plan in the report

The report's rule for choosing a search method:
- If more than a few percent of single edits keep the door working, plain local search wins.
- If working neighbours are rare but a graded score tracks how close a door is to working, use STOKE-style search.
- Otherwise, use macro-moves.

The census lands in the third case for size. About 3% of edits to existing blocks survive, but they are nearly all neutral, the core is rigid, and the current graded score is flat. Next steps:

- **Size:** search needs multi-block moves, such as paired edits and swapping in whole modules. It also needs a richer graded score before STOKE-style search is worth trying.
- **Speed:** single-edit search does find real wins on some doors. A cheap next step is to run the same census for speed across all 58 valid doors.

Throughput note: about 10 designs per second across 4 simulators on a laptop that was already busy (load average of about 6 before the run).
