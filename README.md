# Piston Door Bench

Frontier LLM agents design minimal-volume Minecraft piston doors. A headless Minecraft Java 26.3 engine grades every design: it checks that the door opens and closes reliably, keeps the doorway flush, and fits in as small a box as possible.

## Layout

| Path | What it holds |
|---|---|
| `grader/` | The grader: `pdgrader` (Python rules, validation, grading, kits, run server) and `kernel/` (a Java harness that steps the vanilla 26.3 server tick by tick, plus the physics-patching agent) |
| `phase0/` | First measurements of vanilla piston and redstone timing, and rulebook v0 |
| `runs/pilot*`, `runs/inspect`, `runs/labdev` | Pilot runs and harness development |
| `runs/bench/w1` … `w8` | Benchmark waves: one folder per agent run, with its log, final design and grade |
| `runs/bench/dashboard`, `runs/bench/figures` | Data and page sources for the results dashboard and figures |
| `runs/bench/video` | Rendered film and real-Minecraft recordings of the Opus 5,236 4×4 door |
| `runs/bench/search_pilot` | Search experiments on the agents' doors: the single-edit census and the speed census |
| `reports/`, `research_notes/` | Research reports and the notes behind them |

`.gitignore` leaves out third-party files that scripts fetch, such as the Minecraft server and client jars, the JDK, and the libraries. It also leaves out raw screen captures and rendered frames.

## About the history

This repository was created on 16 November 2026, after the work was done. Its commits were rebuilt from file modification times. Each file enters the history at the time it was last changed, and is dated to that time. Earlier versions of a file were never saved, so they don't appear.
