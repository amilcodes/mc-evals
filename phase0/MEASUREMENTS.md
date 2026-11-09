# Phase 0 measurements

Measured 2026-11-09 on an Apple M4 laptop (10 cores, 16 GB), macOS, single runs unless noted.
Scripts are in `scripts/`; server working directories are in `run/`.

## Pinned platform

| Item | Value |
|---|---|
| Game version | Minecraft Java 26.3 (release, 2026-09-15), world data version 5023, data pack format 121 |
| Server jar | `server.jar`, 62,294,556 bytes, SHA-1 `33680f5f2ac32864d6d7cf5e56a705fdb3e05f4c`, from piston-data.mojang.com |
| Java | Required: 25 (per Mojang's version metadata). Used: Temurin JRE 25.0.5+8 |
| Mod loader availability | Fabric lists 26.3 as stable (loader 0.20.1; Fabric API 0.166.0+26.3). Carpet has a 26.3 build. Neither was downloaded or run. |

26.3 is the latest release; 26.4 is in snapshots.

## Dedicated server (`scripts/bench_server.py`)

| Measurement | Result |
|---|---|
| Cold boot (creates a flat world) | 5.5 s |
| Warm boot (world exists) | 4.7–6.1 s over three boots |
| Shutdown | 0.6–1.0 s |
| Memory (RSS) after boot, `-Xms1G -Xmx2G` | about 820 MB |
| `/tick sprint`, empty flat world | about 22,700 ticks/s |
| `/tick sprint`, 16 pistons cycling continuously | about 4,500 ticks/s |
| 64 pistons | about 3,100 ticks/s |
| 256 pistons | about 1,300 ticks/s |
| 512 pistons | about 540 ticks/s |

The piston workload is a stress case, heavier than a door: every piston is driven by a
two-observer clock and moves a block every few ticks for the whole run. A door fires each
piston a handful of times per open/close.

## Tick-control semantics (matter for exact grading)

- `/tick freeze` then `/tick sprint N` advances **N + 1** ticks, not N (10 → 11, 1 → 2, 1000 → 1001,
  checked with `/time query gametime`). The game returns to frozen afterwards.
- `/tick step N` advances exactly N ticks, but at the target tick rate: at the default 20/s,
  about 600 ticks took 30 s. Raising `/tick rate` (maximum 10000) speeds it up; 2,000 steps
  completed within 3 s at 1000/s and at 10000/s, which is an upper bound because my polling was slow.
- Consequence: a command-driven grader must use `step` (with a raised tick rate) for exact
  counts, or compensate for sprint's extra tick. An in-process grader avoids the issue.

## Built-in headless test runner (`net.minecraft.gametest.Main`)

Invocation: `java -DbundlerMainClass=net.minecraft.gametest.Main -jar server.jar --packs <dir> --tests <selector> --report <xml>`.
Options present in 26.3: `--packs`, `--tests`, `--report`, `--repeatCount`, `--universe`, `--verify`.

| Measurement | Result |
|---|---|
| Runs without `eula.txt` | Yes |
| 4 tests, end to end | 4.2–5.0 s wall (0.4–0.5 s of that is the tests) |
| 500 tests | 7.1 s wall (1.8 s tests) |
| 2,000 tests | 8.5 s wall (4.2 s tests) |
| One test that idles for 20,000 ticks | 6.2 s wall (1.8 s test), so over 11,000 ticks/s |
| `--verify` on one test (100 runs × 4 rotations = 400) | 6.2 s wall, 400/400 passed |
| Exit code | Number of failed required tests |
| Report | JUnit-style XML, one `<testcase>` per run, `<failure message=…>` with world position |

So the fixed cost is about 4.3 s of JVM and world start-up, and tiny tests cost about 2 ms each
after that. Tests run in batches of 50.

Probe tests (`scripts/make_probe_pack.py`): start block → dust → accept block (passes);
start block → piston pushes stone → observer → accept block (passes); start and accept with
nothing between (times out as intended).

### Findings that change the grader design

1. **The runner places tests at a different, far-out world position every run**
   (for example 2080145, 4, −6355711 then −12295973, 4, 8246111). A door whose behaviour
   depends on position could pass on one run and fail on the next. The stock runner therefore
   cannot give a verdict "at one pinned position" without a mod that fixes the position.
2. **Block-based tests only report pass/fail via test blocks.** They cannot return per-tick
   doorway diffs or the swept bounding box. Those need in-process access to the world, so the
   real grader needs a small mod (Fabric supports 26.3) or a command-driven dedicated server.
3. **Experimental redstone is off in the vanilla test server.** Read by reflection from the
   26.3 jar (`scripts/Flags.java`): the test server enables `vanilla` and `trade_rebalance`
   only; `redstone_experiments` and `minecart_improvements` are excluded. A normal dedicated
   server lists only the `vanilla` pack and offers no others. Fabric's own test-server wrapper
   was not checked.
4. **The structure file schema changed.** In 26.3 a palette entry is `{id, properties}`.
   The older `{Name, Properties}` form is accepted without error and silently placed as air.
   `scripts/nbt_structure.py` writes the 26.3 form. Third-party schematic libraries need
   checking against this before use.

## Cost per graded design (estimate from the above)

A time-capped door needs on the order of 1,000–2,000 ticks across several open/close cycles.
At 3,000+ ticks/s under piston load that is under one second of simulation. Start-up adds
4–5 s if each design gets a fresh JVM, so a long-lived server or batched runs are worth it:
2,000 small tests cost 8.5 s in one batch.

## Not measured

- Linux or Docker timings (the Docker daemon was not running); these are native macOS numbers.
- A real door. The workloads are synthetic.
- Determinism beyond 400 repeats of one trivial piston structure.
- Fabric or Carpet on 26.3 (not downloaded).
- Parallel servers on one machine.
