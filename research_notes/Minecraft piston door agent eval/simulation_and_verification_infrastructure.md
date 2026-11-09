# Simulation and verification infrastructure for a piston-door agent benchmark (Minecraft Java Edition, as of Nov 2026)

Reading notes for the report writer:
- "Cited Findings" are things I read in a source this session. Where I only saw a search-engine summary of a page (not the page itself), the bullet says "(search summary only)".
- "Inferences" are my reasoning. Bullets tagged **[background, not verified this session]** are from my prior knowledge of Minecraft tooling and were not confirmed against a source in this session; treat them as leads to verify, not as findings.
- No software was run and nothing was benchmarked in this session. Every throughput number that would matter for sizing is a gap.

## 1. Vanilla Java server options: GameTest, data-driven tests, headless gametest server, `/tick`, Carpet/Scarpet

### Takeaway
The unmodified Mojang server jar is the only backend found with guaranteed piston fidelity, and since 1.21.5 it ships a headless test runner (`net.minecraft.gametest.Main`) that loads structures from a datapack, runs them with a tick timeout, emits a JUnit-style XML report, and can re-run every test 100 times per 90-degree rotation. Block-based (pure datapack) tests can only pass/fail via redstone-triggered test blocks, so "dump the grid and compare open/closed over several cycles" needs either a function test registered by a Fabric/NeoForge mod or a command-driven harness using `/tick freeze` + `/tick step`.

### Cited Findings

**Version naming and unobfuscated jar**
- Mojang's year-based numbering starts with 26.1 (first drop of 2026; hotfixes are 26.1.1 etc.). PaperMC states Mojang "is no longer providing obfuscated server jars" and that Paper "fully dropped the internal remapper"; it also warns that tooling assuming versions start with "1." must be updated — [PaperMC 26.1 announcement](https://papermc.io/news/26-1)
- 26.1 Snapshot 1 was the first snapshot released with only an unobfuscated build — [Minecraft Wiki: Java Edition 26.1 Snapshot 1](https://minecraft.wiki/w/Java_Edition_26.1-snapshot-1)
- 26.1 ("Tiny Takeover") is reported as released 24 March 2026 and is the first version to require Java 25 (release date from one hosting-blog source only) — [WinterNode 26.1 guide](https://winternode.com/blog/minecraft/java/26-1-tiny-takeover)
- Later 2026 versions exist: the `/tick` wiki page's history references "26.3 Snapshot 1" and the GameTest page references 26.2 snapshots, so by Nov 2026 the line has moved to at least 26.2 release / 26.3 development — [Minecraft Wiki: Commands/tick](https://minecraft.wiki/w/Commands/tick), [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest)

**GameTest framework (vanilla)**
- History: GameTest references appeared in 1.15 (19w34a, mostly stripped), code exposed for modders in 1.17 (21w13a), and in 1.21.5 (25w03a) the framework was "overhauled and introduced for datapacks" — [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest)
- A test instance is a JSON file in the `test_instance` registry (`data/<namespace>/test_instance/<name>.json`) naming an environment, a structure, and a type (`block_based` or `function`) — [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest), [Minecraft Wiki: Test instance definition](https://minecraft.wiki/w/Test_instance_definition)
- Test instance fields: `environment` (ID or inline), `structure` (resource location), `max_ticks` (timeout), `setup_ticks` (default 0; wait after placing structure), `required` (default true), `rotation` (`none`/`clockwise_90`/`180`/`counterclockwise_90`), `manual_only`, `sky_access` (default false — "The test is otherwise enclosed in barrier blocks"), `max_attempts` (default 1), `required_successes` (default 1), `type` — [Minecraft Wiki: Test instance definition](https://minecraft.wiki/w/Test_instance_definition)
- Block-based tests use four Test Block modes: Start (emits a redstone pulse when the test starts), Log, Fail (fails when powered), Accept (passes when powered); on a race the first activated wins — [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest)
- Function tests call built-in Java test functions registered in the `test_function` registry; the wiki says they are "meant mainly for Mojang internal use and for mod developers" (package `net.minecraft.gametest.framework`), i.e. a datapack alone cannot define one — [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest); the 1.21.5 changelog likewise says function tests need a mod to register the function — [Minecraft.net: Java Edition 1.21.5](https://www.minecraft.net/article/minecraft-java-edition-1-21-5)
- Test environments group tests and set preconditions (game rules, time, weather; `minecraft:default` is empty). Environment schema has kept changing: 1.21.11 merged `bool_rule`/`int_rule` into `rules`; 26.1 replaced `time_of_day` with `clock_time`; 26.2 added `minecraft:difficulty` — [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest)
- `/test` subcommands: `run`, `runmultiple`, `runclosest`, `runthat`, `runthese`, `resetclosest`/`resetthat`/`resetthese`, `locate` (changelog also lists `runfailed`, `verify`); running/creating a test places a Test Instance Block — [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest), [Minecraft.net: Java Edition 1.21.5](https://www.minecraft.net/article/minecraft-java-edition-1-21-5)
- **Headless runner in the vanilla server jar:** `java -DbundlerMainClass="net.minecraft.gametest.Main" -jar server.jar [options]` starts a server, runs the tests, and exits. Options: `--packs <path>` (datapacks), `--report <path>` (JUnit-like XML), `--tests <selection>` (wildcard on namespaced IDs), `--universe <path>` (test world dir, replaced if it exists; default `gametestserver`), `--verify <boolean>` ("runs the specified tests 100 times per 90-degree rotation step"). Exit code = 0 on all pass, number of failures otherwise, -1 if the server shut down before tests started, 1 on crash — [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest)

**Fabric / NeoForge gametest**
- Fabric: server game tests use Minecraft's framework and "run automatically with the `build` Gradle task"; enable via Loom `fabricApi { configureTests { ... } }`; test classes are registered under the `fabric-gametest` entrypoint; `@GameTest` methods take a `GameTestHelper` (documented example uses `context.setBlock(0,0,0, Blocks.AIR)`, `context.assertBlockPresent(Blocks.AIR, 0,0,0)`, `context.succeed()`) — [Fabric docs: Automated Testing](https://docs.fabricmc.net/develop/automatic-testing)
- Fabric API javadoc (0.119.2+1.21.5): add `-Dfabric-api.gametest` to JVM args to run the server with GameTest enabled; set `fabric-api.gametest.report-file` to export results; the javadoc says this server behaves like a normal dedicated server "except that all experimental features are turned on by default" (search summary only — this matters because the Redstone Experiments pack is an experimental feature; verify before relying on Fabric's gametest launcher for vanilla-default redstone) — [Fabric API javadoc: gametest v1](https://maven.fabricmc.net/docs/fabric-api-0.119.2+1.21.5/net/fabricmc/fabric/api/gametest/v1/package-summary.html)
- Fabric also has *client* game tests (`runClientGameTest`, screenshots via `context.takeScreenshot`, XVFB on Linux CI) — relevant only if rendered-image seamlessness checks are wanted — [Fabric docs: Automated Testing](https://docs.fabricmc.net/develop/automatic-testing)
- Generic CI runners exist that boot a headless server/client per mod loader and MC version: `headlesshq/mc-server-test` and `3arthqu4ke/mc-runtime-test` (search summary only) — [mc-runtime-test GitHub Action](https://github.com/marketplace/actions/mc-runtime-test)

**`/tick` (vanilla, 1.20.3+)**
- Added in 1.20.3 (23w43a); permission level 3; Java only; cannot be run from a command block — [Minecraft Wiki: Commands/tick](https://minecraft.wiki/w/Commands/tick)
- `tick freeze` halts ticking for most gameplay, but "actions not handled by the per-tick loop, such as opening a door, flipping a lever, or changing powered redstone dust, still happen" — [Minecraft Wiki: Commands/tick](https://minecraft.wiki/w/Commands/tick)
- `tick step [<time>]` runs the given number of ticks then refreezes (only valid while frozen; default 1 tick since 23w44a). `tick sprint [<time>]` runs "as fast as possible for the given duration plus one tick", then restores the previous state and prints tick-time performance data. `tick rate` accepts 1.0–10000.0 TPS. `tick query` reports average and percentile time per tick — [Minecraft Wiki: Commands/tick](https://minecraft.wiki/w/Commands/tick)
- In 26.3 Snapshot 1, `/tick step`, `/tick step stop`, `/tick sprint stop` changed from "printing an error and returning 0" to signalling a command error — a harness that parses these must be version-aware — [Minecraft Wiki: Commands/tick](https://minecraft.wiki/w/Commands/tick)

**Carpet / Scarpet**
- Scarpet world-access functions: `set(pos, block, property?, value?, ..., block_data?)`, `block(x,y,z)`, `block_state(block[, property])`, `block_data(pos)` (NBT), `update(pos)`, `block_tick(pos)`, `random_tick(pos)`, `without_updates(expr)`, `place_item(item, pos, facing?, sneak?)` (acts as a player would), `add_chunk_ticket(pos, type, radius)`, `plop(pos, what)` — [fabric-carpet docs: BlocksAndWorldAccess.md](https://raw.githubusercontent.com/gnembon/fabric-carpet/master/docs/scarpet/api/BlocksAndWorldAccess.md)
- Scarpet auxiliary functions: `game_tick(mstime?)` "Causes game to run for one tick" (docs warn that calling it from inside a tick "may lead to artifacts" because it pauses the current tick, runs an inner tick, then finishes the outer one); `tick_time()`; `schedule(delay, function, args...)` (runs at end of tick, in scheduling order); `run(expr)` executes a vanilla command and returns intercepted output; `read_file`/`write_file` support `nbt` and `json` types; `logger(...)` — [fabric-carpet docs: Auxiliary.md](https://raw.githubusercontent.com/gnembon/fabric-carpet/master/docs/scarpet/api/Auxiliary.md)
- Scarpet apps can auto-load from disk at server start if they define `__config()`; Carpet's `/tick warp` accelerates game time and since v1.4.18 has no duration limit (search summary only) — [Fabric Carpet documentation index](https://docsearch.algolia.com/mcp/docs/repo/gnembon/fabric-carpet)
- The SubTick mod (Carpet-ecosystem) lets you step *within* a tick, through individual piston block events — useful for debugging grader disagreements, not for bulk grading — [SubTick on GitHub](https://github.com/chiraagChakravarthy/SubTick)

### Inferences
- **Can vanilla GameTest load an arbitrary structure NBT, run N ticks, and assert block states?** Loading: yes (a structure resource in a datapack passed via `--packs`). Run N ticks with timeout: yes (`max_ticks`, `setup_ticks`). Assert: in a pure-datapack block-based test, only indirectly — the pass/fail signal is "an Accept/Fail test block got powered", so the grader would have to wrap the agent's door in a checking circuit (e.g. observers/comparators at the doorway), which is fragile and cannot express "all 9–49 doorway cells are air, then all solid, three cycles in a row". A **function test in a thin Fabric/NeoForge mod** is the natural way to express the door predicate directly in Java.
- **[background, not verified this session]** `GameTestHelper` exposes helpers such as `pullLever`, `pressButton`, `runAtTickTime`/`runAfterDelay`, `assertBlockState`, `succeedWhen`, `startSequence().thenExecuteAfter(...)`. Only `setBlock`, `assertBlockPresent`, `succeed` were confirmed in the Fabric docs this session.
- Because 26.1+ jars are unobfuscated, a custom test-function mod (or even a small Java agent/launcher that calls into `net.minecraft.gametest.framework` directly) no longer needs mapping toolchains; this lowers the cost of the "thin Java harness on vanilla code" option materially compared with pre-2026.
- `--verify true` (100 runs x 4 rotations) is close to a ready-made determinism/orientation-robustness check, and `max_attempts`/`required_successes` give a native "must pass k of n" knob.
- The barrier-box enclosure (`sky_access: false`) means test structures are isolated from each other; pistons cannot push barriers **[background, not verified this session]**, so designs cannot interfere across tests, but a design that relies on pushing blocks outside its declared bounding box will behave differently than in open world — which is arguably desired for a bounded benchmark.
- Scarpet is sufficient to write the whole grader loop inside the server (place blocks, flip input via `set`/`place_item`, advance ticks, scan the doorway, write JSON). The `game_tick()` caveat means the cleaner pattern is an event/`schedule`-driven state machine combined with `/tick sprint` or Carpet warp, not a blocking loop calling `game_tick()`.
- `/tick freeze` semantics have a subtle consequence: toggling the input lever while frozen will immediately propagate instantaneous effects (dust power levels), while scheduled ticks and block events (repeaters, pistons) wait for the next `step`. This is fine and deterministic, but the grader spec should define "tick 0" as the first stepped tick after the input change.

### Gaps
- No measured boot time for a headless vanilla/gametest server and no measured ticks/sec under `/tick sprint` or Carpet warp were found; searches returned only generic hosting-blog material. Needs a local measurement (boot-to-ready, sprint TPS in a void world with K doors active).
- Could not confirm from a primary page whether the wiki's Test instance definition omits fields (it did not list `function` or padding-related fields; the wiki text itself looked slightly inconsistent in places).
- NeoForge GameTest docs (`runGameTestServer`) were not fetched; NeoForge's status on 26.x not confirmed.
- Fabric Carpet's supported-version status on 26.x was not confirmed (Carpet historically tracks snapshots quickly, but I did not verify a 26.x build).
- The Fabric "all experimental features on by default" statement was seen only in a search summary of the 1.21.5 javadoc; current behaviour on 26.x unverified.
- The exact latest stable release in Nov 2026 (26.2.x vs 26.3) was not pinned down.

## 2. Is vanilla redstone deterministic? Sources of non-determinism and location/direction dependence

### Takeaway
Vanilla redstone is essentially deterministic for a fixed build at a fixed world position and orientation, but its behaviour can legitimately differ between positions and orientations ("locationality"/"directionality") because several orderings come from hash-keyed collections; pistons are affected via block-event ordering and the order in which moved blocks are removed/updated. A grader should therefore pin coordinates and orientation for the official verdict and optionally test translations/rotations as a separate robustness score.

### Cited Findings
- Tick phase order (per `ServerWorld.tick()`, documented for roughly 1.17–1.19): weather, scheduled block/fluid ticks, raids, chunk tick (incl. random ticks), **block events**, entities, block entities, then player inputs — [TechMC Docs: Game Tick](https://techmcdocs.github.io/pages/GameTick/)
- Block events are stored in an `ObjectLinkedOpenHashSet` ("a linked hash set ... This list is used for iteration"); chained events are appended to the end "allow[ing] chaining multiple blockevents in the same tick"; an event is skipped if the block's state no longer matches — [TechMC Docs: Game Tick](https://techmcdocs.github.io/pages/GameTick/)
- The same page nevertheless concludes: "The order in which block events happen is both locational and directional since it is stored in a hashset." (Note the tension: a *linked* hash set iterates in insertion order; the page's own text supports insertion-order iteration, so the locational claim for block events should be treated as the community's summary rather than a derived fact.) — [TechMC Docs: Game Tick](https://techmcdocs.github.io/pages/GameTick/)
- Pistons start extending/retracting in the block-event phase; block events run in creation order and the piston re-validates when the event executes ("a retraction can't fail") — [TechMC Docs: Piston](https://techmcdocs.github.io/pages/Blocks/Piston/)
- When a piston moves a structure, the game builds move/break lists and processes them in a defined order (furthest lines first, ties by fixed axis order), but for removing old blocks "the order of the state updates here is locational" because positions are read out of a hashmap — [TechMC Docs: Piston](https://techmcdocs.github.io/pages/Blocks/Piston/)
- Short pulses: an interrupted sticky-piston extension makes the directly pushed block arrive immediately and "the retraction does not pull the block and therefore it is dropped"; achievable with 0-, 1-, or 2-tick pulses — [TechMC Docs: Piston](https://techmcdocs.github.io/pages/Blocks/Piston/); the wiki likewise notes Java pistons "finish extending early and start retracting if given a pulse shorter than 3 game ticks" — [Minecraft Wiki: Piston/Technical components](https://minecraft.wiki/w/Piston_head)
- Random ticks happen in the chunk phase (3 blocks per subchunk per tick by default) — [TechMC Docs: Game Tick](https://techmcdocs.github.io/pages/GameTick/)
- **Redstone Experiments (1.21.2, snapshot 24w33a):** an experimental data pack, not enabled by default, that reworks redstone wire so it works "the same, independent of position and orientation". In 24w33a a wire line powered from the side "randomly chooses one of two possible update orders"; 24w34a added a left-first tie-break, leaving random only cases where "wire gets powered from above or below without enough context" — [Minecraft.net: Snapshot 24w33a](https://www.minecraft.net/article/minecraft-snapshot-24w33a), [Minecraft.net: Snapshot 24w34a](https://minecraft.net/en-us/article/minecraft-snapshot-24w34a), [Minecraft Wiki mirror: Redstone Experiments (Nov 2025 dump)](https://wiki.ronlab.site/content/minecraftwiki_en_all_maxi_2025-11/Redstone_Experiments)
- Mojang stated that the experiment's "removal of excessive neighbor updates around wire affects the behavior of Quasi-Connectivity based contraptions" — [Minecraft.net: Snapshot 24w34a](https://minecraft.net/en-us/article/minecraft-snapshot-24w34a)
- Paper's Alternate Current patch notes describe the vanilla baseline the same way: under alternative wire implementations "any contraption whose behavior depends on location in vanilla will work everywhere or nowhere" — [Paper: Alternate Current patch](https://ayakael.net/mirrors/papermc/commit/14d355612eceeb4db74dca08fbdef41076003bdc)
- Vanilla's own `--verify` mode (100 runs per 90-degree rotation) shows Mojang treats repeat-run and rotation stability as something to test for rather than assume — [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest)
- A 2026 MDPI paper describes "an engineering method for deterministic verification implemented within a non-deterministic game engine, using controlled clock injection" for validating redstone logic gates against truth tables (search summary only; page returned 403) — [MDPI Electronics 15(3):499](https://www.mdpi.com/2079-9292/15/3/499)

### Inferences
- **[background, not verified this session]** The classic source of redstone-dust locationality is that default (non-experimental) wire collects the positions to update into a `HashSet<BlockPos>` whose iteration order depends on absolute coordinates; this is what makes some dust-fed piston layouts work at one position and fail at another.
- With the Redstone Experiments pack *off* (vanilla default), behaviour is a pure function of (build, absolute position, orientation, tick phase at which input toggles) — no RNG is involved in dust or pistons. With the pack *on*, Mojang's own notes say some orders are random, so **the experimental pack should be explicitly disabled** in the grader world (and Fabric's gametest launcher, which reportedly turns experiments on, needs checking).
- Controls a grader should apply: (a) fixed world type (void/superflat), fixed seed, fixed paste coordinates and facing; (b) `randomTickSpeed 0`, no mobs, weather/daylight cycle off, so nothing stochastic touches the build (matters if designs include e.g. copper, crops, or daylight sensors — or simply ban such blocks); (c) all relevant chunks force-loaded before paste and the paste confined away from chunk borders if possible (chunk-boundary effects on update propagation are a known community concern — not sourced this session); (d) define input toggle at a fixed sub-tick point (command executed between ticks while frozen); (e) run each open/close cycle several times and require identical grids each cycle; (f) optional robustness metric: re-run at 4 rotations and a handful of translations (including odd/even and negative coordinates, across a chunk border) and report the pass fraction — expert doors are sometimes knowingly locational/directional, so this is better as a secondary score than a hard requirement.
- Pasting itself is a determinism hazard: the order in which blocks are placed and whether placement triggers neighbour updates decides whether QC-powered pistons, BUD states, and half-extended states exist at t=0. The harness should paste with updates suppressed where possible, then apply a defined "settle" period (e.g. `setup_ticks`) and require the door to be in its declared initial state before the first toggle.

### Gaps
- No primary source this session for the pre-1.21.2 wire `HashSet` mechanism or for chunk-position-dependent block-event ordering; the techmcdocs pages are undated (c. 1.17–1.19) and may not reflect 26.x internals. With unobfuscated 26.x jars this can now be checked directly in `ServerLevel`, `RedStoneWireBlock`, `PistonBaseBlock`, `PistonStructureResolver`.
- Status of Redstone Experiments in 26.1–26.3 (still an opt-in experimental pack, changed, or merged) could not be confirmed; the wiki copy found was a Nov 2025 mirror stating it is not enabled by default.
- No source found quantifying how often real expert piston doors are locational/directional.

## 3. MCHPRS and Redpiler: piston support and fidelity scope

### Takeaway
MCHPRS does not implement pistons — the "piston implementation" request was labelled `wontfix` by the lead maintainer in 2021 and closed as not planned — so it (and anything built on its Redpiler backend) is unusable as a piston-door grader despite being the fastest redstone simulator available.

### Cited Findings
- MCHPRS describes itself as "A Minecraft 1.20.4 creative server built for redstone"; "many things that are a part of Vanilla Minecraft servers don't exist here"; MIT licence; ~2.3k stars, 1,221 commits, no tagged releases — [MCHPR/MCHPRS README](https://github.com/MCHPR/MCHPRS)
- Redpiler pre-computes all redstone connections, so "interaction with the world is limited in this state"; placing or breaking blocks while it runs resets and disables it; `--optimize` "can, and will, break the state of your build" — [MCHPR/MCHPRS README](https://github.com/MCHPR/MCHPRS)
- Issue #48 "piston implementation" (opened 20 Jul 2021): contributor AL1L wrote "Pistons will require a lot of work and probably some refactoring to add them"; maintainer StackDoubleFlow added `enhancement` then `wontfix` ("This will not be worked on") on 9 Nov 2021; closed as "not planned" 6 Aug 2022 — [MCHPRS issue #48](https://github.com/MCHPR/MCHPRS/issues/48)
- Issue #102 "Cant place basic Redstone components (Observer, pistons, slime etc.)" is closed (Aug 2024); the repo was still active in 2026 (PR #241 opened 3 May 2026) — [MCHPRS issues search: piston](https://github.com/MCHPR/MCHPRS/issues?q=piston)

### Inferences
- Redpiler's architecture (compile a static connection graph, forbid world mutation) is structurally incompatible with moving blocks, which is consistent with the wontfix decision; this is unlikely to change.
- MCHPRS remains relevant only for non-piston sub-circuits (e.g. validating a door's control logic in isolation), which is not what this benchmark needs.

### Gaps
- Did not read `docs/Redpiler.md` or the block list in source to enumerate exactly which components are supported (observers, slime as inert blocks, etc.); the README itself does not mention pistons either way.
- Did not check forks (e.g. `pluetonical/mchprs-modified` appeared in search listings) for piston support.

## 4. Other reimplementations and whether they implement piston / block-event mechanics faithfully

### Takeaway
No non-Mojang implementation found is a credible vanilla-accurate piston simulator as of Nov 2026: the Rust/Java reimplementations either have no vanilla mechanics (Minestom), broken or immature pistons (Pumpkin), or a deliberately different redstone engine (Cuberite), and Nucleation's simulation path is MCHPRS Redpiler. Paper runs Mojang's piston code but patches exploit-adjacent piston behaviour by default.

### Cited Findings

| Backend | Pistons / moving blocks | Evidence |
|---|---|---|
| Vanilla server jar (Mojang) | Yes — reference implementation | n/a |
| Fabric / NeoForge on vanilla | Yes (vanilla code; loaders add hooks only) | [Fabric docs](https://docs.fabricmc.net/develop/automatic-testing) |
| Paper / Folia | Yes, but patched: `allow-piston-duplication: false`, `allow-headless-pistons: false`, `allow-permanent-block-break-exploits: false` by default, under an "unsupported settings" section that "may be removed at any time" | [Paper global configuration reference](https://docs.papermc.io/paper/reference/global-configuration/) |
| MCHPRS | **No** (wontfix) | [issue #48](https://github.com/MCHPR/MCHPRS/issues/48) |
| Nucleation | Simulation via MCHPRS Redpiler → **no pistons** by inheritance (not stated explicitly on its page) | [Schem-at/Nucleation](https://github.com/Schem-at/Nucleation) |
| Pumpkin (Rust) | **Broken/immature** | below |
| Minestom | **No** vanilla redstone at all | below |
| Cuberite (C++) | Has its own redstone simulator; not vanilla-accurate | below |
| Valence, Glowstone, Feather | Unknown — nothing found | Gap |

- **Paper redstone:** `redstone-implementation` selects vanilla, Eigencraft, or Alternate Current (vanilla is the default when unset). Patch notes say both alternatives "reorder redstone updates heavily" and that location-dependent contraptions "will work everywhere or nowhere" under them — [Paper: Alternate Current patch](https://ayakael.net/mirrors/papermc/commit/14d355612eceeb4db74dca08fbdef41076003bdc)
- **Paper piston-related settings:** `allow-piston-duplication` (TNT/carpet/rail duping; default false), `allow-headless-pistons` (default false), plus `block-updates.disable-*` toggles; Paper also carries a patch titled "Fix piston physics inconsistency MC-188840" — [Paper global configuration reference](https://docs.papermc.io/paper/reference/global-configuration/), [Paper patch 0422](https://ayakael.net/mirrors/papermc/src/commit/017af785ff3ca4925e91f9e1b9a2cf7b2a26b6e7/patches/server/0422-Fix-piston-physics-inconsistency-MC-188840.patch)
- **Pumpkin:** a third-party status write-up titled "Pumpkin runs Minecraft on 100MB but pistons don't work" reports pistons, sticky pistons and block swapping as broken while wire, repeaters, comparators, observers are complete — [Botmonster: Pumpkin status](https://botmonster.com/self-hosting/pumpkin-minecraft-server-in-rust-status/); Pumpkin's own redstone issue listed pistons as not working at all with a fix in progress — [Pumpkin issue #766](https://github.com/Pumpkin-MC/Pumpkin/issues/766); a guide updated 5 Sep 2026 says Pumpkin is not yet a fit for servers with redstone contraptions — [RespawnHost: Pumpkin vs Paper/Vanilla](https://respawnhost.com/en/wiki/games/pumpkin-minecraft/pumpkin-vs-paper-vanilla/)
- **mscts** (a 2026 conformance suite comparing a candidate server — Pumpkin — against vanilla tick-by-tick at packet level) has a pistons group covering push limit, immovable blocks, sticky pulls, slime/honey and quasi-connectivity; method: freeze the world, set up with commands, step a fixed number of ticks, compare block events/updates/block-entity data per tick; reference tier must self-agree 20/20. Issue opened 30 Sep 2026, closed 23 Oct 2026 — [ericbstie/mscts issue #40](https://github.com/ericbstie/mscts/issues/40)
- **Minestom:** a library, not a server; "does not implement vanilla gameplay"; the community `BasicRedstone` extension covers only power propagation, doors/trapdoors, buttons/levers (last pushed 2021); `VanillaReimplementation` is a limited WIP — [Minestom docs: What is Minestom](https://minestom.net/docs/what-is-minestom), [TogAr2/BasicRedstone](https://github.com/TogAr2/BasicRedstone)
- **Cuberite:** maintainers say "the redstone simulator in Cuberite is a bit different than in Vanilla, there's a lot of corner cases in Vanilla that aren't matched"; quasi-connectivity was added by a dedicated PR — [Cuberite forum](https://forum.cuberite.org/printthread.php?tid=3006), [cuberite PR #4889](https://github.com/cuberite/cuberite/pull/4889)
- **Nucleation:** "A Minecraft schematic engine in Rust: load, build, simulate, mesh, and render schematics from seven languages"; MIT; bindings for Rust, JS/TS (npm, WASM), Python 3.12+, plus Kotlin/JVM, PHP, C, C++; redstone simulation via "MCHPRS redpiler" with "typed circuit executors"; also advertises a "vanilla-accurate tick loop, verified against captures from the game", GLB/glTF/USDZ meshing and a headless renderer, and a Verilog→`.schem` "Redstone EDA" toolchain. ~25 stars — [Schem-at/Nucleation](https://github.com/Schem-at/Nucleation). The crates.io build excludes simulation because MCHPRS is not on crates.io (git-only feature) — [docs.rs: nucleation](https://docs.rs/crate/nucleation/0.10.8)
- **schemsmith** (Python, 2026): has an in-repo redstone simulator whose pistons originally responded to power and QC "but they don't move blocks"; block movement (push limit, immovable blocks, slime/honey, sticky retraction) was added 1 Nov 2026 for a "2×2 piston door module", explicitly excluding "0-tick and block update tricks" — [syrianah/schemsmith issue #16](https://github.com/syrianah/schemsmith/issues/16)
- A browser "Minecraft Redstone Circuit Designer & Simulator" advertises QC for pistons under Java rules; open-source status unknown (search summary only) — [craftmc.net tool](https://www.craftmc.net/tools/minecraft-redstone-circuit-designer)

### Inferences
- The make-or-break column collapses the field: only code that *is* Mojang's `PistonBaseBlock`/`PistonMovingBlockEntity` (vanilla, Fabric, NeoForge, and — with caveats — Paper) is safe for expert-level doors, which routinely use 0-tick/1-tick block dropping, QC/BUD powering, observer chains and slime/honey structures. Hand-written simulators (schemsmith, Cuberite, Pumpkin) explicitly skip or mismatch exactly these behaviours.
- Paper is a defensible second choice only if `redstone-implementation: vanilla` and the unsupported piston toggles are enabled; even then its piston patches (MC-188840 fix, dupe fixes) mean "matches vanilla" is not guaranteed. For a benchmark whose ground truth is "works in vanilla", using Paper buys nothing over Fabric/vanilla unless Bukkit plugins are specifically needed.
- Nucleation's "vanilla-accurate tick loop, verified against captures from the game" is a claim worth a direct test with a piston door before ruling it in or out — the README did not say whether that loop covers pistons. Independently of simulation, Nucleation looks useful as the schematic I/O + meshing/rendering layer (and it runs in WASM, e.g. for an agent-side preview tool).
- mscts is the most relevant *methodological* precedent found: its freeze → command setup → step N → compare-per-tick recipe is exactly the grader loop, and its piston test groups could serve as a conformance suite if anyone later wants a fast non-JVM grader validated against vanilla.
- A fast approximate simulator (schemsmith-style) could still be valuable as an *agent-side tool* (cheap inner-loop feedback) with the vanilla server as final judge; the gap between the two then becomes part of what the benchmark measures.

### Gaps
- Valence (Rust), Glowstone, Feather: no sources found this session on piston support. **[background, not verified]** Valence is a framework without built-in vanilla mechanics, Feather is archived, and Glowstone has long been stalled on old versions.
- Folia-specific redstone behaviour (regionised ticking) was not researched.
- Did not verify Pumpkin's piston status against the live repo in Nov 2026 (third-party write-ups and an older issue only).
- No open-source, standalone, vanilla-verified piston simulator (JS/Python/Rust) was found; absence of evidence after ~3 targeted searches, not proof of absence. Community tools living only on Discord would not surface in web search.

## 5. Bot/automation APIs for driving a real server: paste, trigger, step exactly N ticks, dump the grid

### Takeaway
The most robust loop is server-side: load the design as a structure template (or place it from an in-server mod/Scarpet app), freeze ticking, toggle the input with a command, advance with `/tick step N`, and read the doorway region from inside the server process (mod test function or Scarpet) rather than through a network bot. Network clients such as Mineflayer add chunk-sync latency and cannot observe sub-tick state reliably.

### Cited Findings
- `/tick freeze` + `/tick step <n>` give exact N-tick advancement from 1.20.3; `/tick` needs permission level 3 and cannot be issued from a command block — [Minecraft Wiki: Commands/tick](https://minecraft.wiki/w/Commands/tick)
- Vanilla headless gametest runner takes datapacks containing structures and test instances and writes a JUnit-style report — [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest)
- Scarpet `run(expr)` executes any vanilla command and returns captured output; `set`/`block_state`/`block_data` read and write blocks in-process; `read_file(..., 'nbt')` loads an NBT file; `write_file(..., 'json')` can emit results — [fabric-carpet docs: Auxiliary.md](https://raw.githubusercontent.com/gnembon/fabric-carpet/master/docs/scarpet/api/Auxiliary.md), [BlocksAndWorldAccess.md](https://raw.githubusercontent.com/gnembon/fabric-carpet/master/docs/scarpet/api/BlocksAndWorldAccess.md)
- Mineflayer: `bot.blockAt(point)` returns a Block or `null` if the chunk is not loaded on the client; a `blockUpdate` event exists — [Mineflayer world-interaction docs (mirror)](https://tessl.io/registry/tessl/npm-mineflayer/4.32.0/files/docs/world-interaction.md), [Mineflayer API docs (mirror)](https://git.tdem.in/PrismarineJS/mineflayer/blob/master/docs/api.md)
- prismarine-schematic can `paste(world, at)` into a prismarine-world and `makeWithCommands(offset, platform)` to emit vanilla commands that build a schematic — [PrismarineJS/prismarine-schematic](https://github.com/PrismarineJS/prismarine-schematic)
- mscts drives vanilla with "the world is frozen, set up with commands, and stepped a fixed number of ticks" and compares packets per tick — evidence this pattern works at tick-exact granularity over the protocol — [ericbstie/mscts issue #40](https://github.com/ericbstie/mscts/issues/40)

### Inferences
Ranked options for the four steps (my assessment):

| Approach | (1) Paste | (2) Trigger | (3) Exact N ticks | (4) Dump grid | Robustness |
|---|---|---|---|---|---|
| **A. Thin Fabric (or NeoForge) mod registering one generic test function**, run via vanilla/Fabric gametest server | structure from datapack (one test instance per submission) | helper sets lever / redstone block at declared input pos | framework tick callbacks | iterate doorway `BlockPos`, read `BlockState` in-process, write JSON | Highest; batch-parallel; JUnit report; rotations/verify built in |
| **B. Vanilla jar + datapack + RCON/stdin**, `/tick freeze`, `/place template`, `/setblock`, `/tick step`, `/execute if blocks` or per-cell `/execute if block` | `/place template ns:name x y z` | `/setblock` lever state or redstone block | `/tick step N` then poll `/tick query` | compare doorway to a reference region with `/execute if blocks`, or probe each cell | No mods at all (cleanest licensing/repro story); chatty; needs care that step finished before reading |
| **C. Fabric Carpet + Scarpet app** | `set()` per block or `run('place template ...')` | `set()` / `place_item()` | scheduled state machine + tick warp | `block()`/`block_state()` scan → `write_file` JSON | Good; no Java build; depends on Carpet keeping up with MC versions |
| **D. Mineflayer / protocol bot** | `/setblock` spam or WorldEdit | chat command or physical click | `/tick step` via chat | `bot.blockAt` after chunk sync | Lowest; client-side world view lags; `moving_piston` states arrive asynchronously |

- **[background, not verified this session]** Relevant vanilla commands: `/place template <id> <pos> [rotation] [mirror]` (1.19+), `/setblock`, `/fill`, `/clone`, `/data get block` (block-entity NBT only — not block state), `/execute if block <pos> <predicate>`, `/execute if blocks <start> <end> <dest> (all|masked)`, `/forceload add`. Structure templates saved by structure blocks are limited to 48×48×48, but templates loaded from datapacks/NBT files can be larger. RCON has per-packet payload limits, so large dumps should be chunked or written server-side.
- A robust dump must handle the transient `minecraft:moving_piston` block (block 36): at the sampling tick, a doorway cell may be `moving_piston` rather than air or the final solid block. The verdict should be taken after a quiescence check (no `moving_piston` anywhere in the bounding box and grid unchanged for K consecutive ticks), with a max-tick budget per transition.
- The input should be standardised by the benchmark (e.g. "a lever at declared position P" or "the grader places/removes a redstone block at P"), because physically "pressing" a button requires a player/fake player (Carpet fake players or `GameTestHelper` helpers), while a `setblock` of `lever[powered=true]` does trigger neighbour updates. **[background, not verified]**
- Baritone and `mcpi` (Raspberry-Pi API / RaspberryJuice) are not good fits: Baritone is a client pathfinding/building bot (slow, survival-style placement), and `mcpi` has no tick control or block-state fidelity. Neither was researched in depth this session.

### Gaps
- `/place template`, `/execute if blocks`, `/data get block`, `/forceload` semantics and the 48³ structure-block limit were not re-verified against the wiki this session.
- RCON response-size limits and whether `/tick step` returns before or after the ticks complete over RCON were not sourced.
- No source found for an off-the-shelf Fabric mod exposing an HTTP "paste/step/dump" API suited to this; the search did not surface one.
- Mineflayer's protocol support for 26.x was not checked.

## 6. Schematic formats and libraries

### Takeaway
For a vanilla-server grader the natural interchange target is the vanilla structure `.nbt` (directly loadable by GameTest and `/place template`); Sponge `.schem` and `.litematic` are what the redstone community and most libraries speak. A simple agent-facing JSON/Python block-list that the harness converts to `.nbt` avoids depending on any one third-party library's version coverage.

### Cited Findings
- Sponge Schematic Specification: current version is 3 (dated 2021-05-04; main change is 3D biome support); NBT, GZip-compressed; root holds a `Schematic` compound with required Width/Height/Length; recommended extension `.schem` — [SpongePowered/Schematic-Specification](https://github.com/SpongePowered/Schematic-Specification)
- `mcschematic` (Python, Apache-2.0): `MCSchematic().setBlock((x,y,z), "minecraft:stone")`, `.save(folder, name, mcschematic.Version.JE_1_18_2)`; version enum covers "every version of Minecraft since Java Edition 1.9"; block-entity NBT supported; writes WorldEdit schematic files (Sponge version not stated); small repo (14 commits) — [Sloimayyy/mcschematic](https://github.com/Sloimayyy/mcschematic)
- `litemapy` (Python): reads and writes Litematica `.litematic` with full block storage; only dependency is `nbtlib` — [litemapy on PyPI](https://pypi.org/project/litemapy/), [SmylerMC/litemapy](https://github.com/SmylerMC/litemapy)
- `nbtlib` (Python): general-purpose NBT read/edit library (not schematic-specific) — [vberlier/nbtlib (via relatedrepos)](https://relatedrepos.com/gh/vberlier/nbtlib)
- `prismarine-schematic` (JS, MIT): reads Sponge v1–v3 and MCEdit; writes Sponge v2 only; no Litematic; has `paste`, `makeWithCommands`, `forEach` — [PrismarineJS/prismarine-schematic](https://github.com/PrismarineJS/prismarine-schematic)
- `mc_schem` (Rust): covers `.litematic`, vanilla structure `.nbt`, WorldEdit `.schem` (1.13+) and `.schematic` (≤1.12) — [docs.rs: mc_schem](https://docs.rs/mc_schem)
- Nucleation (Rust + Python/JS/WASM, MIT): load/save/edit schematics, SNBT round-trips, data-version migration, diff/fingerprint analysis, meshing; examples use `.schem` — [Schem-at/Nucleation](https://github.com/Schem-at/Nucleation)
- Scarpet can read `.nbt` files directly inside the server — [fabric-carpet docs: Auxiliary.md](https://raw.githubusercontent.com/gnembon/fabric-carpet/master/docs/scarpet/api/Auxiliary.md)

### Inferences
- **[background, not verified this session]** The vanilla structure format is simple enough to emit by hand with `nbtlib`: a gzip NBT compound with `size` [x,y,z], `palette` (list of `{Name, Properties}`), `blocks` (list of `{pos, state, nbt?}`), `entities`, and `DataVersion`. Writing this directly (~50 lines of Python) removes library risk, and `DataVersion` must match (or be older than and upgradable to) the server version.
- Recommended pipeline: agent emits a constrained JSON/Python description — list of `{pos:[x,y,z], block:"minecraft:sticky_piston", state:{facing:"up", extended:"false"}}` plus declared `doorway` box, `input` position/type, and `closed_block` — harness validates against a block allow-list and the server's block-state registry (reject unknown IDs/properties *before* booting anything), then writes `.nbt`. Volume (bounding box of non-air blocks, or of the declared box) and block count fall out of the same parsed list with no simulator needed.
- Accepting `.litematic`/`.schem` as *alternative* submission formats (converted via litemapy / mc_schem / Nucleation) is useful mainly for importing human reference doors as baselines.
- Block-state validation is where LLM submissions will most often fail (invalid `facing`, forgetting `extended`, piston-head blocks without bases, `moving_piston` in the initial state). The harness should define whether pre-extended pistons and their `piston_head` blocks are allowed in the initial state and check base/head consistency.

### Gaps
- `amulet-core` and WorldEdit's own CLI/API were not researched this session.
- Did not confirm which Sponge version `mcschematic` writes, nor any of these libraries' support for 26.x data versions / block IDs.
- Vanilla structure NBT layout above is from memory; the wiki's "Structure file" page was not fetched.

## 7. Performance and scale; licensing constraints for shipping a harness

### Takeaway
No hard throughput numbers were found, so capacity planning needs a quick local benchmark; architecturally, batching many submissions into one long-lived server (GameTest places tests side-by-side in one world) amortises JVM boot and should make thousands of designs tractable. On licensing, the safe pattern — used by itzg's Docker image — is to never redistribute Mojang's jar: download it at runtime and require the user to accept the EULA.

### Cited Findings
- `/tick sprint <time>` runs ticks as fast as hardware allows and reports achieved performance; `/tick rate` caps at 10000 TPS — [Minecraft Wiki: Commands/tick](https://minecraft.wiki/w/Commands/tick)
- Vanilla gametest server runs all selected tests in one process and exits with the failure count; `--tests` wildcard selects subsets; `--universe` dir is recreated each run — [Minecraft Wiki: GameTest](https://minecraft.wiki/w/GameTest)
- 26.1+ requires Java 25 — [WinterNode 26.1 guide](https://winternode.com/blog/minecraft/java/26-1-tiny-takeover)
- itzg/minecraft-server downloads the server software at container start (not baked into the image), requires `EULA=TRUE`, keeps jar/world under `/data`, and supports `TYPE=CUSTOM` jars — [itzg docker-minecraft-server env docs (mirror)](https://mintlify.com/itzg/docker-minecraft-server/configuration/environment-variables)
- The Minecraft EULA's core rule is not to distribute anything Mojang has made; it applies to "client and server versions of Minecraft"; things others make (mods/tools) are not covered by that restriction provided they don't themselves violate the EULA (2014 law-firm commentary; the live EULA page timed out) — [Mudd Law: Navigating the Minecraft EULA](https://blog.muddlawoffices.com/2014/05/25/navigating-the-minecraft-eula), [Minecraft EULA](https://minecraft.net/eula)
- Since 26.1 the jar is unobfuscated, so harness code can be written against real names without shipping mappings — [PaperMC 26.1 announcement](https://papermc.io/news/26-1)
- MCHPRS, Nucleation, prismarine-schematic are MIT; mcschematic is Apache-2.0 — [MCHPRS](https://github.com/MCHPR/MCHPRS), [Nucleation](https://github.com/Schem-at/Nucleation), [prismarine-schematic](https://github.com/PrismarineJS/prismarine-schematic), [mcschematic](https://github.com/Sloimayyy/mcschematic)

### Inferences
- Per-design tick budget is small: a 3x3–7x7 door cycle is on the order of tens to a few hundred game ticks; with, say, 3 open/close cycles and settle periods, ~1–2k ticks per design. Even at a conservative few hundred TPS for a world containing many active doors, that is seconds per design, and GameTest runs many test structures concurrently in one tick loop — so the dominant cost is likely JVM/server boot (amortised by batching) and structure placement, not ticking. **These are estimates, not measurements.**
- Two deployment shapes: (i) *batch* — write N submissions as N structures + N test instances into a generated datapack, launch one gametest server, parse XML/JSON; (ii) *service* — one long-lived server with a mod/Scarpet endpoint that accepts designs into a free grid slot. Shape (i) is simpler and hermetic (fresh world per batch); shape (ii) gives low latency for agent tool-calls during an episode. A benchmark probably wants both: (ii) as the agent's in-episode "test my door" tool and (i) for final scoring.
- Isolation between concurrent tests: space slots so no two bounding boxes share a chunk-update neighbourhood, and remember piston push limits/slime structures can extend beyond the declared box; GameTest's barrier enclosure plus spacing handles this.
- Licensing posture for a published harness: ship only your own code (datapack generator, mod source/jar that contains no Mojang classes, Dockerfile); fetch the server jar from Mojang's official download endpoint at build/run time; require explicit EULA acceptance (as itzg does). Pre-26.1 the "Mojang mappings" licence was a separate redistribution concern; with unobfuscated jars the practical issue reduces to "don't redistribute the jar or decompiled source". **This is my reading, not legal advice, and the live EULA text was not retrieved.**
- Pin the exact Minecraft version in the benchmark spec (e.g. "Java Edition 26.x.y"), since redstone/piston behaviours and the GameTest JSON schema have both changed across 1.21.5 → 26.2.

### Gaps
- **No sourced numbers** for: headless server boot time, memory footprint of a void-world gametest server, achievable TPS under `/tick sprint`/Carpet warp, or tests-per-second through GameTest. All need measurement.
- The current official EULA text (and any 2025–2026 changes accompanying deobfuscation) was not read; the redistribution summary relies on old commentary plus the itzg design.
- GameTest's concurrency limits (tests per batch, grid layout/spacing parameters) were not found in the sources read.

## 8. Programmatically checking "seamlessness" / visual indistinguishability

### Takeaway
No existing tool for redstone-specific seamlessness or exposed-component detection was found; this will have to be defined and implemented by the benchmark, most simply as block-state equality of the wall plane(s) against a uniform reference, with an optional stricter visibility test done by voxel raycasting or by rendering.

### Cited Findings
- Vanilla can compare two regions natively: the grader could build a reference "closed wall" region and compare with block-region predicates (command semantics not re-verified this session; see Gaps) — pointer: [Minecraft Wiki: Commands/tick](https://minecraft.wiki/w/Commands/tick) for the freeze/step half of that loop
- Nucleation provides meshing (GLB/glTF/USDZ) and "a headless renderer" for schematics, runnable from Python/JS/WASM — a possible basis for rendering closed/open states from fixed viewpoints without a game client — [Schem-at/Nucleation](https://github.com/Schem-at/Nucleation)
- Fabric client game tests can launch a real client under XVFB, wait for chunk render, and `takeScreenshot` — the highest-fidelity (and slowest) way to get true rendered views — [Fabric docs: Automated Testing](https://docs.fabricmc.net/develop/automatic-testing)
- The piston-door community has a formal classification scheme (door size, type restrictions, wiring restrictions, pattern) that appears to define terms like seamless/flush/hipster (search summary of a Scribd-hosted rules document only; not read) — [Scribd: piston door rules document](https://www.scribd.com/document/820662283/Rule)
- The wiki's piston tutorial describes the "smallest 3x3 seamless door" as "fully hidden, no pistons or redstone visible" — i.e. community usage ties "seamless" to visibility of components, not only to the doorway cells — [Minecraft Wiki: Tutorial: Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses)

### Inferences
- A tiered, fully programmatic definition is feasible from the dumped block grid alone:
  1. **Doorway check:** all WxH doorway cells (through the full declared wall thickness) are air when open; all are `closed_block` (full, opaque, non-component) when closed.
  2. **Flush/seamless wall check:** in the closed state, every cell of the front (and back) wall plane within a margin around the doorway equals the uniform wall block; in the open state, same except the doorway. Equivalent to diffing the plane against a reference.
  3. **No-exposed-components check ("hipster"-style strictness):** flood-fill air from the player-accessible half-spaces (front, back, and through the open doorway); flag any cell adjacent to reachable air whose block is in a "redstone component" set (pistons, dust, repeaters, observers, slime/honey, etc.). A stricter line-of-sight variant casts rays (3D DDA / Amanatides–Woo voxel traversal) from a grid of eye positions in the walkable volume and flags components hit before an opaque full cube; this needs a per-block opacity/full-cube table (glass, slabs, stairs are not occluders).
  4. **Rendered check (optional):** render closed-state front/back and compare to a render of a plain wall (pixel diff), via Nucleation's headless renderer or Fabric client gametest screenshots.
- Tiers 1–3 need only the grid and a small block-property table (derivable from the game's data reports, **[background, not verified]** `java -DbundlerMainClass=net.minecraft.data.Main -jar server.jar --reports`), so they add negligible cost per design. Tier 3 should be evaluated in both the open and closed states and ideally at mid-transition is *not* required (most community definitions concern rest states).
- Visibility of *transient* states (e.g. piston heads flashing in the doorway during opening) is a separate aesthetic criterion; decide explicitly whether the benchmark scores it.

### Gaps
- No search was run specifically for general voxel occlusion/visibility libraries, and none surfaced incidentally; the raycasting/flood-fill approach above is a design proposal, not an existing tool.
- The community's exact definitions of seamless / flush / hipster / full-hipster were not retrieved from a primary source in this session (another researcher may be covering taxonomy).
- `/execute if blocks` semantics not re-verified.

## 9. Existing projects that automatically test, search or optimise redstone contraptions (tooling and non-LLM baselines)

### Takeaway
I found no public tool that automatically searches for or optimises piston doors (no SAT/GA "piston door solver"), and no LLM benchmark that verifies piston contraptions by simulation; the nearest neighbours are a 2026 SAT encoding of piston-free redstone logic, Nucleation's Verilog-to-schematic flow, and 2026 agent-oriented projects (schemsmith, mscts) that build tick-exact redstone test harnesses. Non-LLM baselines will likely have to be human expert doors from community archives.

### Cited Findings
- "Redstone with SAT solvers" (alloc.dev, 9 Jan 2026): author "formalized redstone (meaning dust, torches, and blocks) into CNF notation, so I could make SAT solvers create redstone circuitry"; motivating example a full adder. Components modelled are dust, torches and solid blocks — no pistons (aggregator copy; original returned 403) — [alloc.dev: Redstone with SAT solvers](https://alloc.dev/2026/01/09/redstone_from_sat) via [scour.ing copy](https://scour.ing/@matmat/p/https://alloc.dev/2026/01/09/redstone_from_sat)
- Nucleation "Redstone EDA" compiles Verilog into simulation-verified `.schem` files (reports 18 artifacts, 221,785 blocks, 2,660 verification checks) — computational redstone, not piston mechanisms — [Schem-at/Nucleation](https://github.com/Schem-at/Nucleation)
- schemsmith (Python, active Nov 2026) is building, in numbered phases, toward a "2×2 piston door module" with its own simulator and per-rule timing tests; it explicitly excludes 0-tick and block-update tricks — [syrianah/schemsmith issue #16](https://github.com/syrianah/schemsmith/issues/16)
- mscts (2026) is a tick-exact vanilla-conformance suite with a piston group; labels on its issues (`opus`, `scrutiny::high`) suggest it is developed with LLM coding agents — [ericbstie/mscts issue #40](https://github.com/ericbstie/mscts/issues/40)
- MDPI Electronics 2026, "Digital Twin for Designing Logic Gates in Minecraft Through Automated Circuit Verification and Real-Time Simulation": truth-table verification of redstone logic gates with controlled clock injection (search summary only) — [MDPI Electronics 15(3):499](https://www.mdpi.com/2079-9292/15/3/499)
- "MineCEraft: Evaluating Language Models as Construction Engineers in the World of Minecraft" (arXiv 2608.28884): 723 expert-written instructions, programmatically verifiable evaluation, 17 task categories; whether redstone/pistons are included is not stated in the snippet (search summary only) — [arXiv:2608.28884](https://arxiv.org/abs/2608.28884)
- Human "smallest door" records exist only as forum/wiki/schematic-site artefacts: e.g. the wiki credits a 56-block smallest 3x3 seamless door to SacredRedstone; a MineSchematic upload lists a "Tiny 3x3" door at 1×8×7, 49 blocks for Java 1.21.11; the wiki cautions that "smallest" claims are unreliable because doors "have evolved a lot" — [Minecraft Wiki: Tutorial: Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses), [MineSchematic: Tiny 3x3 Piston Door](https://mineschematic.com/s/tiny-3x3-piston-door-f5336481)
- Two extended searches for piston-door search programs (genetic/evolutionary/brute-force/sequence solver) returned only build guides and schematic sites — no solver — [example result set: Minecraft Forum "Smallest hidden piston doors?"](https://www.minecraftforum.net/forums/minecraft-java-edition/redstone-discussion-and/330028-smallest-hidden-piston-doors)

### Inferences
- The absence of public piston-door search tools is plausible for technical reasons: the state space (block placement × block states × timing) is huge and the transition function (vanilla piston/update semantics) is expensive and only available inside the JVM — exactly the infrastructure gap this benchmark's harness would fill. Once a fast batch grader exists, simple non-LLM baselines become possible: (a) human expert doors imported from `.litematic`/`.schem`; (b) local-search "shrinkers" that delete/merge blocks from a working human door while the grader still passes; (c) template-parameterised generators for small sizes.
- **[background, not verified this session]** The technical community does use bespoke programs for sub-problems — notably piston-extender retraction-sequence search (finding pulse sequences for N-extenders) — typically shared in Discord servers and YouTube descriptions rather than indexed repos. I could not surface any via web search, so treat their existence/availability as unconfirmed here.
- SAT/SMT encodings so far cover only static combinational redstone (dust/torch/block); extending them to pistons would require modelling block events and moving blocks, which nobody appears to have published.
- The appearance of several 2026 projects pairing LLM agents with tick-exact redstone verification (schemsmith, mscts, Nucleation's EDA flow) suggests the "agent + simulator-in-the-loop" pattern is emerging, but none targets expert-level piston doors or publishes a benchmark for them.

### Gaps
- Could not read the SAT article, the MDPI paper, or the MineCEraft paper directly (403 / snippet only); details above are from search summaries or an aggregator copy.
- Community Discord-hosted tools (piston-sequence solvers, door archives' internal validation bots) are invisible to web search; someone with access to the relevant Discords (e.g. piston-door catalogue communities) should check for automated verification bots and solver tools.
- No GitHub code search was performed (e.g. `piston door solver`, `extender sequence`); a direct GitHub/YouTube search may still find small unindexed repos.
