# Speed census: greedy timing search on every valid door

The census ran on all 54 doors that ended a benchmark run valid, waves 1–9. Each door was searched under the physics it was built for.

## The search

1. Every timing edit to every signal component was tried. The edits:
   - a repeater's other delays;
   - a repeater swapped for an observer, comparator or wire;
   - an observer's other facings, or the observer swapped for a repeater;
   - a comparator swapped for a repeater, observer or wire;
   - wire swapped for a repeater.
2. The edits that made the door faster were applied one at a time, best first. Each was kept only if the door still passed, was no larger, and had strictly fewer open + close ticks.
3. Steps 1 and 2 were repeated, up to 3 rounds.
4. Every result was then re-checked with the final grade (8 cycles with offset flips), 11 placement shifts and a 180° turn.

Script: `speed_census.py`. Results: `speed_census.jsonl`. Faster designs: `speed_designs/`.

## Results

| | |
|---|---|
| Doors searched | 54 |
| Faster at the same volume | **35** |
| …at least as robust as the original | 35 (34 pass everything; one was already 7/11 on placements and stays so) |
| Median cut in open + close ticks, among improved doors | 14% |
| Largest cut | 49% (Opus 216 changed-physics 3×3: 35/32 → 20/14) |
| Edits per improved door | median 2, max 8 |

### Biggest speedups

| Door | Volume | Before (open/close ticks) | After | Edits |
|---|---:|---|---|---:|
| Opus 3×3, changed physics (`w5-3x3p-opus-c`) | 216 | 35/32 | **20/14** | 3 |
| Sonnet 3×3 (`w1-sonnet-b`) | 405 | 114/60 | 62/40 | 6 |
| Sonnet 3×3 (`w3-sonnet-d`) | 720 | 60/32 | 36/16 | 4 |
| Opus 3×3 (`w9-3x3-std-b-opus`) | 729 | 44/58 | 30/38 | 8 |
| Opus 3×3 (`w1-opus-b`) | 312 | 46/16 | 30/15 | 6 |
| Opus 4×4, kit 2 (`w7-4x4k2-opus-c`) | 396 | 82/82 | 60/60 | 6 |
| Fable 4×4 (`w2-4x4-fable-a`) | 264 | 90/66 | 70/60 | 3 |
| Fable 3×3 (`w1-fable-a`) | 70 | 34/22 | 28/16 | 1 |

## Reading

- **Agents tune for volume, not speed.** Two thirds of their doors leave easy timing gains. Most gains come from swapping a delay-4 repeater for a shorter one or an observer.
- **Tight doors have little room.** No speedup was found for the smallest designs: the Opus 140 3×3, both 72-volume changed-physics Fable doors, and the 2×2 and 3×2 doors. Their timing is already set by the mechanism, not by spare delay.
- **Human records are still far faster.** A 72-volume 3×3 opens in 0.6 s (12 ticks); the best agent 70 opens in 28 even after search. Closing that gap needs a different mechanism, not retiming. That fits the single-edit census: these doors are irreducible under one-block changes.
