# Wave 9: Opus 3×3, standard vs changed physics, 50-minute limit

Six Opus 5.5 runs started together on the same harness and kit 1. Three used standard rules and three used changed physics: repeater step 3 ticks, observer delay 3 ticks. Wave 9 repeats wave 8 with a 50-minute limit instead of 120. Each agent could get the neutral continue message up to 3 times. All six used all three.

All six doors pass the strict final grade (8 cycles, offset flips). Total cost: $47.52.

| Run | Physics | Final volume | First valid door | Cost |
|---|---|---:|---:|---:|
| std-a | standard | **140** | 25.5 min | $7.54 |
| std-c | standard | 495 | 20.7 min | $7.70 |
| std-b | standard | 729 | 23.1 min | $8.12 |
| chg-c | changed | **126** | 22.9 min | $7.91 |
| chg-a | changed | 384 | 26.3 min | $8.96 |
| chg-b | changed | 1,950 | 30.2 min | $7.29 |

## What it does to the physics comparison

| | Standard | Changed | Std ÷ changed (geometric mean) | One-sided permutation p |
|---|---|---|---:|---:|
| Waves 1–8 (120 min) | 80, 154, 216, 264, 312, 360, 520 | 70, 112, 112, 112, 216, 264 | 1.77 | 0.05 |
| Wave 9 alone (50 min) | 140, 495, 729 | 126, 384, 1,950 | 0.81 | 0.55 |
| Pooled, waves 1–9 | median 288 (n = 10) | median 126 (n = 9) | 1.35 | 0.23 |

Wave 9 does not replicate the earlier gap. The changed-physics doors are still not worse; their median remains lower. But the pooled evidence that they are *smaller* drops from p = 0.05 to p = 0.23. The defensible claim is now **"changed physics did not hurt Opus"**, not **"changed physics helped"**.

Two caveats:
- **Different time limits.** Wave 9 ran 50 minutes against 120, so pooling mixes budgets.
- **Wide spread within a setting.** Variance inside each setting (126 to 1,950 at 50 minutes) is far larger than the gap between settings. Sharper estimates need many more runs per arm.

## Other observations

- **Faster first doors.** Every run had a valid door by minute 31. That is faster than wave 8's 40–67 minutes, likely because the shorter limit pushes agents to build sooner.
- **Early stops.** Every agent stopped early, at 9–15 minutes left each time, and judged the next size cut too risky.
- **Continue messages paid off three times:**
  - std-a: 154 → 140
  - chg-b: no door → 2,250 → 1,950
  - chg-a: 432 → 384
- **Gaps agents reported in TASK.md:**
  - A torch is not read as a comparator side input.
  - Repeaters need a supporting block.
  - Dust step-connections make accidental links easy.
  - The hallway tube spans every z.
  - Which blocks a lever can attach to (an observer works, a piston does not).
