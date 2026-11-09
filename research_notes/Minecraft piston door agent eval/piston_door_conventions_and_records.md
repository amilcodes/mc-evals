# Piston door conventions, taxonomy, metrics and records in the technical-redstone community (as of 2026-11-09)

Research method note: the authoritative rule text was read directly from the Redstone Squid GitHub repo (`reference/Door_Rules.md`, MIT-licensed, repo last pushed 2026-11-09). Record figures come mostly from YouTube video titles/descriptions written by the record builders themselves (primary but self-reported), cross-checked where possible against the Minecraft Wiki and against "door list" Google Docs published by CraftyMasterman and Purplers. Reddit could not be fetched (403 / blocked) and Discord (#record-logs) is not web-readable, so the live Squid record list itself was NOT read. Rule definitions below are paraphrased, not verbatim.

Source short-names used below:
- [Squid Rules] = https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md
- [Rules for Dummies] = https://docs.google.com/document/d/1a0xI0Pj6lKlULCmVr9n4GH2jnpjDXal4HeiJGhzRF0s/edit
- [Wiki Piston uses] = https://minecraft.wiki/w/Tutorial:Piston_uses (revision last edited 2 Nov 2026)
- [Squid repo] = https://github.com/redstone-squid/Redstone-Squid

---

## 1. What are the standard door categories and their exact definitions (seamless, flush, hipster, trapdoor, funnel, tileable, ...)?

### Takeaway
There is one formal, actively maintained ruleset: the "Squid Records – Rules" document used by the Redstone Squid bot/Discord. It names a door as `<wiring placement restrictions> <animated restrictions> <size> <type> <orientation>` plus a subtitle of `<component restrictions> <miscellaneous restrictions>`. In that ruleset "seamless" is about what is visible *inside the hallway* (no circuitry visible, in tiers by state), while "flush"/"trapdoor"/"deluxe"/"hipster" are about *where the circuitry sits relative to the outer wall/floor/ceiling surface*; the Minecraft Wiki's looser glossary agrees in spirit but is less precise.

### Cited Findings
**Naming grammar**
- Title = `<wiring placement restrictions> <animated restrictions> <size> <type> <orientation>`; subtitle = `<component restrictions> <miscellaneous restrictions>`. Worked example in the rules: a flush seamless full-sync 5x5 iris funnel trapdoor, subtitle no slimes/honey/observers, directional. — [Squid Rules §2.1](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- A "piston door" is defined as an *entrance* whose hallway is only horizontal or vertical and is "continuable" (the hallway pattern can continue past the wiring indefinitely). An "entrance" is an opening connecting two rooms via a hallway plus the wiring that opens/closes it; one interaction with the input toggles open/closed. Staircases, tree entrances, pillar trapdoors are "entrances", not piston doors. — [Squid Rules §2.1, §2.2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- A build must have exactly one input device controlling everything, and every function must be reachable with a single use of it. — [Squid Rules §2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)

**Size token (`<size>`)**
- `<size>` is the minimal set of dimensions describing the opening inside the door frame: `m × n × k` (width × height × depth), `m × n`, or "m wide"/"n high" for expandable/tileable doors. A 16×16 funnel is still called "16×16" though its door blocks span 16×16×8. — [Squid Rules §2.1.1](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)

**Type (`<type>`) – four independent axes, combinable**
- (1) Arrangement of door blocks (default REGULAR): REGULAR, FUNNEL, ASDJKE, CAVE, CORNER, DUAL CAVE CORNER, STAIRCASE, GOLD PLAY BUTTON, VORTEX, PITCH, BAR; modifiers VERTICAL, REVERSED, INVERTED (funnel flipped front-to-back), DUAL (mirrored so it looks the same from both sides; needs frame depth ≥ 2). VAULT is an alias for DUAL FUNNEL. — [Squid Rules §2.1.2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- (2) Composition of door blocks (default "quartz-like" blocks): IRIS, ONION, STARGATE, FULL STARGATE, FULL LAMP, LAMP, SISSY BAR, CHECKERBOARD, WINDOWS, REDSTONE BLOCK CENTER, SAND (sand/gravel/concrete powder), GLASS (glass blocks, not panes), GLASS STRIPE, CENTER GLASS, ALWAYS ON LAMP. — [Squid Rules §2.1.2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- (3) Hallway shape: CIRCLE, TRIANGLE, RIGHT TRIANGLE, BANANA, DIAMOND, SLAB-SHIFTED. (4) Hallway composition: RAIL, DUAL RAIL, CARPET, SEMI TNT, FULL TNT, HIDDEN (lamp/sand). — [Squid Rules §2.1.2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- "Quartz-like blocks" = blocks that could be swapped for quartz without breaking the build: opaque, pushable/pullable, conductive, not gravity-affected. — [Squid Rules §5](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- The bot's seed data lists 42 official "pattern" tags (regular, funnel, asdjke, cave, corner, …, full_tnt) matching the list above. — [Squid repo seed.sql](https://github.com/redstone-squid/Redstone-Squid/blob/master/seed.sql)

**Orientation**
- DOOR = frame faces a cardinal direction; SKYDOOR = frame faces up/down (called FLOOR/CEILING TRAPDOOR when the full-trapdoor placement rule is met). — [Squid Rules §2.1.3](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)

**Wiring-placement restrictions (the seamless/flush/hipster family)**
- SEAMLESS: informally, standing in the hallway you cannot tell the door is there; formally the hallway must match the type's hallway composition, i.e. no circuitry visible inside the hallway. Four tiers — SUPER, FULL, SEMI, QUART — defined by which of five conditions hold: front side of closed door blocks / when opened / when closed / during opening / during closing; the two strictness levels are "no circuitry AND no entities visible" vs "no circuitry visible". — [Squid Rules §2.1.4](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Simplified tiers: FULL SEAMLESS = no redstone visible once the door has finished opening or closing; SEMI SEAMLESS = seamless only when closed or only when open. — [Rules for Dummies §1.1](https://docs.google.com/document/d/1a0xI0Pj6lKlULCmVr9n4GH2jnpjDXal4HeiJGhzRF0s/edit)
- SUPER SEAMLESS additionally covers the opening/closing animation (wiring not visible during operation as well as at rest) — stated explicitly in the utilities section and in the CLEAN animation rule ("super-seamlessly animated"). — [Squid Rules §2.4, §2.1.5](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- DENTLESS: no protrusions or recessions in the hallway (beyond the type's hallway composition). Non-colliding things (torches, dust, open fence gates, particles) count as protrusions; hoppers / piston-head shafts / missing hallway blocks count as recessions; things that affect player movement (water, repeaters, carpets, cobwebs, fences, walls) disqualify the build from being a recognised door at all. MINOR DENTS ONLY relaxes this to supported non-colliding parts (wall torches, floor dust) and wall/ceiling recessions. — [Squid Rules §2.1.4](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- FULL TRAPDOOR // FLUSH // DELUXE: door blocks sit 0 // 1 // 2 blocks in front of the circuitry, and the circuitry must be at or behind the outer surface. A horizontal full-trapdoor is a WALL TRAPDOOR ("flush layout" is just a wall trapdoor); a vertical one is a FLOOR/CEILING TRAPDOOR. SEMI FLUSH // DELUXE additionally lets circuitry be at or below floor level (not for skydoors). — [Squid Rules §2.1.4](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- HIPSTER: FULL FLOOR // CEILING // WALL HIPSTER = all circuitry behind floor // ceiling // wall level in both stable states; SEMI = circuitry may also be *on* that level. Every floor hipster is semi flush. — [Squid Rules §2.1.4](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- EXPANDABLE (infinitely, or finitely with at least 8 steps): extra layers extend the frame into one bigger door with one input. TILEABLE: repeated tiles each with their own input; FULL TILEABLE tiles never affect neighbours, SEMI TILEABLE tiles can interfere if run simultaneously. M WIDE / N HIGH restrict one machine dimension (e.g. "1 wide"). WEATHERPROOF also exists. — [Squid Rules §2.1.4](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Official restriction tags in the bot's seed data: super/full/semi/quart_seamless, dentless, full_trapdoor, flush, deluxe, flush_layout, semi_flush, semi_deluxe, full/semi floor/ceiling/wall hipster, expandable, full/semi_tileable, no_slime_blocks, no_honey_blocks, no_gravity_blocks, no_sticky_pistons, contained_slime/honey, only_wiring_slime/honey/gravity, no_observers, no_note_blocks, no_clocks, no_entities, no_flying_machines, zomba, zombi, torch_and_dust_only, redstone_block_only, (not_)locational, (not_)directional, locational/directional_with_fixes. — [Squid repo seed.sql](https://github.com/redstone-squid/Redstone-Squid/blob/master/seed.sql)

**Animated restrictions**
- SYMMETRICAL / FULL SYMMETRICAL; SYNCHRONOUS in three tiers (SUPER / FULL / SEMI SYNC — block "sections" retract/extend in unison); CLEAN (no jerky or unnecessary moves); named layouts such as SPIRAL, SHUTTER, SCISSOR. — [Squid Rules §2.1.5](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)

**Minecraft Wiki glossary (looser, general-audience)**
- Flush = can be hidden in a wall on at least one side so the closed surface is flat with the wall; Seamless = circuitry not visible on either side (may still need a recess, so not necessarily flush); Vault door = door blocks occupy a 2-deep or deeper volume; Funnel = one-sided vault; Iris; Sand door; Uncontained = affects things outside its own volume; Entityless; Observerless; Slimeless; Sync; Directional = works only in one orientation; Locational = works only at certain coordinates (chunk-border dependent); 0-reset = can be re-triggered immediately. — [Wiki Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses)
- "Jeb door" = the famous 2×2 flush door first shown by Jeb in the sticky-piston preview (wiki lists it at 72 blocks; a "half Jeb door" 1×2 flush at 36). — [Wiki Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses); Jeb's door dated 14 Jun 2011, modelled on a Keith Majhor design of 6 Jun 2011 — [CraftyMasterman 2x2 timeline doc](https://docs.google.com/document/d/1iz1zYdcQJZ3_MFN8fElV-kCd8cratsy37Q68PvKY3BI/edit)
- Community members describe "hipster" strictly as all redstone below the floor/door, and argue over whether gravity-block doors count. — [r/redstone thread mirror](https://axebps-redlib.hf.space/r/redstone/comments/1jb1g23/3x3_extremely_fast_automatic_open_and_shut) (forum opinion, hearsay-grade)

### Inferences
- "Seamless" (hallway view) and "flush" (relation to an outer wall) are orthogonal in the formal rules; a door can be seamless but not flush (the default record category) or flush and seamless. The colloquial "2×2 flush = Jeb door" matches FULL FLUSH / WALL TRAPDOOR-style placement.
- For a benchmark, the minimal faithful category is "FULL SEAMLESS N×N REGULAR DOOR" (vertical frame, quartz-like door blocks, air when open), optionally with `NO ENTITIES` — this is what the headline "smallest N×N" records mean.
- The Squid ruleset has no category literally called "layered"; the equivalents are M WIDE (e.g. 1-wide), TILEABLE and EXPANDABLE.

### Gaps
- The exact cell values of the 4-tier seamless table (which of the five conditions each of SUPER/FULL/SEMI/QUART requires, and at which strictness) were lost in the markdown export — the table cells are images/symbols in the original Google Doc. QUART SEAMLESS in particular is not defined in text I could read.
- Definitions of ASDJKE, GOLD PLAY BUTTON, VORTEX, PITCH, BAR, ONION etc. exist only as linked images; not captured.
- The "named layout" list (spiral/shutter/scissor…) is in a separate Google Doc that was not fetched.

---

## 2. How is door size measured (bounding box? what is included? block counts? panel/1-wide conventions)?

### Takeaway
Size is always an axis-aligned bounding-box volume, width × height × depth in blocks (air inside the box counts), not a block/component count. In the Squid rules the box is drawn around the *circuitry* accumulated over every state and motion, includes entities, and excludes the door blocks, plain hallway/frame/outer-surface blocks, and the input device.

### Cited Findings
- SMALLEST = no build in the same record category has smaller volume; ties go to the earlier provable completion date. — [Squid Rules §4.2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Volume = width × height × depth of the build's circuitry along x/y/z, rounded up to an integer; both blocks and entities count. — [Squid Rules §4.2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Each dimension is measured cumulatively across all opening/closing operations and both stable states (i.e. the swept volume, so pistons/blocks that poke out mid-animation count). — [Squid Rules §4.2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Exclusions: (1) door blocks, outer-surface blocks, hallway blocks (unless they must be a specific non-default block in the open state), the door frame, and the input device; (2) blocks/entities inside the hallway except in the open state; (3) an entity that would stay inside a one-block shell around the wiring; (4) the part of an entity hitbox that merely sits at a fractional position where a block could still be hand-placed. — [Squid Rules §4.2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- CIRCUITRY = WIRING minus door/outer-surface/hallway blocks that fit the hallway composition; WIRING = the redstone components connected to the single input whose removal would break the build; the INPUT BLOCK (the block the button/lever powers) *is* part of the wiring. — [Squid Rules §5](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Simplified statement: size = width × height × depth, rounded up, entities included; exclude the frame and the input device, and blocks/entities inside the hallway when the door is closed. — [Rules for Dummies §2](https://docs.google.com/document/d/1a0xI0Pj6lKlULCmVr9n4GH2jnpjDXal4HeiJGhzRF0s/edit)
- Expandable builds report volume as an expression with a static control part plus a per-layer part (example in rules: 40+20x blocks for x = 1–14) and state the range of x where it beats the record. A CONTAINED volume conversion (padding uncontained slime/honey) also exists but is defined by a diagram. — [Squid Rules §4.2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- The Minecraft Wiki uses the same idea: size = the volume of a box containing the door, counting empty blocks; it tells readers to always state closing time, opening time, size in blocks and seamless/unseamless, and to distrust words like "smallest"/"compact". — [Wiki Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses)
- Builders report records as `W×H×D = N b` strings, e.g. 5×11×1 = 55 (3×3), 9×1×11 = 99 (4×4), 20×1×10 = 200 (5×5 carpet), 1×22×14 = 308 (6×6), 1×24×15 = 360 (7×7). — [Door_Maker 3x3 tutorial](https://www.youtube.com/watch?v=dxcZcYBB75s), [Cwee 4x4](https://www.youtube.com/watch?v=AUVLmzOYXFU), [Cwee 5x5 carpet](https://www.youtube.com/watch?v=oCPP8LWJyXY), [Cwee 6x6](https://www.youtube.com/watch?v=1Ojxa1Ljj_8), [Cwee 7x7](https://www.youtube.com/watch?v=ipAx9-AOng4)
- Record builders also quote "density" (non-air cells / volume; values above 100% because several entities can share a block), e.g. the 308-block 6×6 has 4 air cells, 98.7% dense without entities and 121.8% with. — [Cwee 6x6](https://www.youtube.com/watch?v=1Ojxa1Ljj_8)
- "Layout size" is used as a theoretical floor: SacredRedstone's 56-block 3×3 was long considered unbeatable because it was layout-sized. — [Purplers 3x3 door list](https://docs.google.com/document/d/1MOT4I41A1mFjLGfK19F5cwNPYSLizsQrUytsIMnnHfM/edit)
- Valid input for records: stone/wooden button or lever, mounted on the surface of the contraption with block support from inside the volume; build must work with both player ("direct") input and repeater input (see MC-172213). The input device itself is excluded from volume. — [Squid Rules §3.1, §4.2](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)

### Inferences
- Because door blocks and hallway blocks are excluded only as *blocks* but the box is an axis-aligned bounding box of the circuitry, the opening itself normally ends up inside the box when wiring sits on both sides of it. E.g. 5×11×1 = 55 for a 3×3 implies an 11-long, 5-tall, 1-deep slab that contains the 3×3 opening plus 4 columns each side and 2 rows above/below combined. So in practice reported volumes are "the whole machine slab including the hole".
- Block counts / component counts are not a ranked metric anywhere in the ruleset; they appear only informally (material lists in tutorials, entity counts, density).
- "1 wide" (M WIDE) is the dominant form factor for size records at every size ≥ 3×3; all current smallest 4×4–10×10 regular records found are 1 block deep.
- A benchmark adopting community rules should measure the bounding box of all non-air, non-hallway blocks swept over open, closed and transitional states, excluding the lever/button — a static closed-state bounding box would under-count versus community practice.

### Gaps
- The CONTAINED-volume conversion diagram was not readable.
- No source found for a community "block count" leaderboard; I believe none exists but cannot prove absence.

---

## 3. What other metrics are ranked (speed, reliability, etc.) and what restrictions attach to records?

### Takeaway
Five record classes exist — FIRST, FASTEST, SMALLEST, FASTEST SMALLEST, SMALLEST FASTEST — with speed compared lexicographically on six timings (opening time first). Reliability, loc/directionality, entity use, slime/observer use etc. are not scored; they are either hard eligibility gates or opt-in restriction tags that define separate record categories.

### Cited Findings
- Record title = `<base title> <record category>`; base titles: FIRST, FASTEST, SMALLEST, FASTEST SMALLEST (fastest among the tied-smallest pool), SMALLEST FASTEST (smallest among the tied-fastest pool). — [Squid Rules §4](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Speed tie-break order for doors/entrances: (1) opening time — input to the last block movement that leaves the hallway in its "open" pattern; (2) opening visible/"seamless" time — input to last visible movement from inside the hallway (z-fighting counts); (3) closing time; (4) closing visible time; (5) opening reset time — from end of opening-visible time until the door can safely be closed again (can be negative); (6) closing reset time. — [Squid Rules §4.3.1](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Timing conventions: measured in game ticks or seconds (20 gt = 1 s), with repeater input; a normal extension or retraction ends 2 gt after it starts, an instant retraction ends when it starts, a 0–2 gt pulse extension ends at start + pulse length; variable-speed doors are ranked by their slowest case. — [Squid Rules §4.3](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- The bot's door table stores exactly four timings per door: normal_opening_time, normal_closing_time, visible_opening_time, visible_closing_time (integers, game ticks implied). — [Squid repo doors table](https://github.com/redstone-squid/Redstone-Squid/blob/master/schema/structure/public/tables/doors/table.sql)
- The wiki notes there are several ways to count opening time and that 2026 community consensus differs from 2013. — [Wiki Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses)
- Eligibility gates (all records): valid single button/lever input that works with player and repeater input; must not become unreliable over time (no unreliable glitches, time-of-day dependence, unreliable mob AI, or wiring that breaks on chunk reload); opening/closing must have a bounded duration (no RNG / random-tick waits); unlimited uses (no manual refilling, not save-state dependent, no entity drift needing readjustment); vanilla only, no cheats needed to build or run; buildable without switching versions; works in at least one *release* of Java Edition; player movement in the hallway must not break it; no non-isolated sensors (sculk, pufferfish); works in the Overworld; and for doors/entrances it must reach at least one SEAMLESS tier. — [Squid Rules §3](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Functionality is judged assuming no lag, all chunks loaded, no weather effects, no world border, no outside mobs. — [Squid Rules §6](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Opt-in component restrictions (each creates its own category): no slime / honey / gravity blocks, no sticky pistons, contained slime/honey, only-wiring slime/honey/gravity, NO OBSERVERS, NO NOTE BLOCKS, NO CLOCKS (no permanently running clock in a stable state), NO ENTITIES (block entities, falling blocks and items still allowed), NO FLYING MACHINES, CONTAINED (still works when surrounded by any mix of air, quartz-like, slime, honey, immovable blocks), ZOMBA / ZOMBI / TORCH AND DUST ONLY / REDSTONE BLOCK ONLY component whitelists. — [Squid Rules §2.1.6](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Misc restrictions: NOT LOCATIONAL // NOT DIRECTIONAL (works at any position / facing), LOCATIONAL // DIRECTIONAL WITH FIXES (a variant exists for every position/facing), UP-TO-DATE (works in the latest version; otherwise the entry is tagged [BROKEN]). A door that is slower at some positions cannot claim both NOT LOCATIONAL and the faster time. — [Squid Rules §2.1.7, §2, §7](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)
- Builders' own descriptors on record videos mirror these tags: "no entities, contained, fully reliable", "not input bugged, no input delay", "not locational or directional", "breaks on paper servers", plus explicit reset times and version ranges. — [Br1ckcraft3r 715b 5x5](https://www.youtube.com/watch?v=eVy2hLuMiSg), [Br1ckcraft3r 540b 5x5](https://www.youtube.com/watch?v=qKYv33Rt71s), [Br1ckcraft3r 55b 3x3](https://www.youtube.com/watch?v=N_yOjRYGA_w)
- Hybrid "smallest door at speed X" / "fastest door at volume Y" titles are common in practice (e.g. "Smallest 0.6s 3x3 (72 blocks)", "Fastest 132b 4x4 (0.9 s)", "Smallest 0.4s 4x4 (308 blocks)"). — [JensundLars](https://www.youtube.com/watch?v=R6e__lLvwrg), [Br1ckcraft3r](https://www.youtube.com/watch?v=LKFnjR6V-a8), [Ya boi immense lad](https://www.youtube.com/watch?v=5tWmnXiCqxY)
- Legitimacy disputes are real: a 21-block 2×2 (2022) was labelled illegitimate because entities stuck out of the volume and a pufferfish could be triggered from the hallway; a 2023 2×2 using non-ticking entities was also ruled not legit; an early 99-block 4×4 version had limited uses because a suffocating allay was not relog-proof. — [Kawediloru](https://www.youtube.com/watch?v=XoTcMq5_57c), [CraftyMasterman 2x2 doc](https://docs.google.com/document/d/1iz1zYdcQJZ3_MFN8fElV-kCd8cratsy37Q68PvKY3BI/edit), [CraftyMasterman 4x4 doc](https://docs.google.com/document/d/1iO0H9vkPXjHwVsbbhnfFPcMnK3TP_SGNZtRMAiXsSSU/edit)

### Inferences
- 0-ticks, quasi-connectivity, update-order dependence and budding are all *allowed* by default; nothing in the rules bans them. The only ways they are constrained are the reliability gate and the optional NOT LOCATIONAL / NOT DIRECTIONAL tags.
- Entities are allowed in the unrestricted "smallest" category, and since 2022 every headline smallest record ≥ 3×3 uses them (minecarts, mobs, fireballs). An agent benchmark that forbids entities should compare against the NO ENTITIES sub-records, which are materially larger.
- "Lag-friendliness", "survival-friendliness" and "spammability" are not formal Squid metrics; the closest formal proxies are reset time (spammability), NO CLOCKS, and the unlimited-uses/reliability gates.
- Non-seamless doors cannot hold Squid records at all (eligibility rule: at least one seamless tier), so "non-seamless smallest N×N" is not an officially tracked category.

### Gaps
- No formal definition found for "input bugged", "input delay", or "cycleless" (terms used on videos); they are community jargon outside the rules text.
- I did not find how moderators verify submissions in practice beyond the bot's vote sessions (schema has vote tables).

---

## 4. Where are records tracked? Any machine-readable database / API / schema?

### Takeaway
The canonical tracker is the Redstone Squid Discord bot and server ("Squid Records"; #record-logs and #build-logs), backed by a PostgreSQL database with an open-source codebase that, as of Aug 2026, also exposes a versioned REST API (`/v1/builds`, `/v1/records`, `/v1/search`, …) and a read-only public web catalogue. The public hostname of that API/catalogue is not in the repo, so I could not query live records; everything else lives in YouTube descriptions, the Synergy creative server, and ad-hoc Google Docs.

### Cited Findings
- Redstone Squid is "a custom bot designed to manage redstone records"; MIT-licensed; repo `redstone-squid/Redstone-Squid` (successor to `Kappeh/Redstone-Squid`), last pushed 2026-11-09; maintainer contact "papetoast". Main bot instance client id 528946065668308992. — [Squid repo README](https://github.com/redstone-squid/Redstone-Squid)
- Records are posted to #record-logs of the Discord server discord.gg/Khj8MyA with creators, description, working versions, media/world-download links and a link to the beaten records stored in #build-logs. — [Squid Rules §1](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md); [Rules for Dummies §5–6](https://docs.google.com/document/d/1a0xI0Pj6lKlULCmVr9n4GH2jnpjDXal4HeiJGhzRF0s/edit)
- Other servers can subscribe: `!settings smallest_channel|fastest_channel|first_channel set #channel`; submissions historically went through a Google Form (`!submit_record`) and are confirmed/denied by admins (`!submissions open|view|confirm|deny`). — [Squid repo README](https://github.com/redstone-squid/Redstone-Squid)
- Legacy relational schema (still in repo): `builds(id, submission_status, record_category, category, width, height, depth, completion_time, submission_time, version_spec, extra_info jsonb, submitter_id, ai_generated, embedding, is_locked, …)`; `doors(build_id, orientation, door_width, door_height, door_depth, normal_opening_time, normal_closing_time, visible_opening_time, visible_closing_time)`; plus `types`, `restrictions`, `restriction_aliases`, `build_types`, `build_restrictions`, `versions`, `build_versions`, `build_creators`, `build_links`, `extenders`, `entrances`, `utilities`, `messages`, `vote_sessions`, `votes`, `users`, `server_settings`. — [builds table](https://github.com/redstone-squid/Redstone-Squid/blob/master/schema/structure/public/tables/builds/table.sql), [doors table](https://github.com/redstone-squid/Redstone-Squid/blob/master/schema/structure/public/tables/doors/table.sql), [schema dir](https://github.com/redstone-squid/Redstone-Squid/tree/master/schema/structure/public/tables)
- Newer schema (Alembic migrations July–Oct 2026): unified tag taxonomy (`tag_definitions` with `semantic_kind` = pattern/restriction, `authority` = official), computed "record competitions"/definitions with a recompute queue, schematic storage and renders, "simulation evidence", build revisions, API keys, a Fabric client mod / Paper plugin / Rust CLI for submitting from in-game. — [alembic versions](https://github.com/redstone-squid/Redstone-Squid/tree/master/alembic/versions), [seed.sql](https://github.com/redstone-squid/Redstone-Squid/blob/master/seed.sql)
- REST API "Redstone Squid API" v1.0.0 (OpenAPI document committed): `GET /v1/builds`, `GET /v1/builds/{build_id}`, `GET /v1/records`, `GET /v1/records/{record_id}`, `GET /v1/search`, `/v1/search/fields`, `/v1/search/suggest`, `GET /v1/tags`, `GET /v1/versions`, `GET /v1/builds/{build_id}/schematics`, `…/schematics/{id}/content`, `…/schematics/render`, `/v1/creators/{id}`, plus auth/submission/vote endpoints. — [contracts/openapi.json](https://github.com/redstone-squid/Redstone-Squid/blob/master/contracts/openapi.json)
- A record result object has: id, definition_id, competition_id, title, subtitle, record_class, build_kind, version_scope, status, holder_build_ids, computed_at (detail adds holder_builds). — [squid/api/v1/schemas/records.py](https://github.com/redstone-squid/Redstone-Squid/blob/master/squid/api/v1/schemas/records.py)
- A bilingual (en / zh-CN) read-only public catalogue (Astro SSR, `/records`, `/builds` pages) was completed 2026-08-11; only `confirmed` builds are public; the plan describes "66 tables, a safe query language, computed record competitions, weighted voting". — [docs/plans/completed/public-catalogue.md](https://github.com/redstone-squid/Redstone-Squid/blob/master/docs/plans/completed/public-catalogue.md)
- Synergy creative server (play.synergyserver.net) hosts a "WR plot" where record doors are physically kept and avogaado's "Redstone Archive"; several 2025–2026 records were built there. — [Cwee, Aug 2026](https://www.youtube.com/watch?v=iD6u2gJwWM0), [avogaado, Jul 2026](https://www.youtube.com/watch?v=YkMhE7cxveM), [Ya boi immense lad](https://www.youtube.com/watch?v=5tWmnXiCqxY)
- redstone-server.info lists member builds with stated volume/speed (hobbyist level, self-described). — [example: 7x7, 4940 blocks](https://redstone-server.info/node/12079)
- Record-history documents with per-door volume/date/link tables: 3×3 (Purplers), 4×4 and 2×2 (CraftyMasterman), 4×4 vault (CraftyMasterman, 2024). — [3x3 list](https://docs.google.com/document/d/1MOT4I41A1mFjLGfK19F5cwNPYSLizsQrUytsIMnnHfM/edit), [4x4 timeline](https://docs.google.com/document/d/1iO0H9vkPXjHwVsbbhnfFPcMnK3TP_SGNZtRMAiXsSSU/edit), [2x2 timeline](https://docs.google.com/document/d/1iz1zYdcQJZ3_MFN8fElV-kCd8cratsy37Q68PvKY3BI/edit), [vault doors](https://docs.google.com/document/d/1MzHQMiV6zIkEGkZB7NvFup_qEnRiLrO0RrGFpz6J8RM/edit)
- YouTube channels that publish record doors with stats in the description: Cwee, Door_Maker, Kawediloru (Ganymede), Br1ckcraft3r, SacredRedstone, PixieBlox, lum3nd0, JensundLars, avogaado, Ya boi immense lad; long-form histories by CraftyMasterman and Purplers. — [YouTube: Cwee 6x6](https://www.youtube.com/watch?v=1Ojxa1Ljj_8), [Purplers](https://www.youtube.com/watch?v=5cYDoWDI7Dw), [CraftyMasterman](https://www.youtube.com/watch?v=1RJnrzZ0Mr8)
- The Minecraft Wiki piston-uses tutorial keeps a small table of notable doors by size with volumes but does not reference Squid. — [Wiki Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses)
- A 6-page "Minecraft Piston Door Regulations" PDF on Scribd is a copy of a Squid-style ruleset (seamless = no circuitry visible inside the hallway when open; volume = width × length × height). — [Scribd](https://www.scribd.com/document/820662283/Rule)

### Inferences
- The benchmark could ingest baselines directly from the Squid API once its hostname is obtained (ask in the Discord or from the maintainer); the OpenAPI file in the repo is enough to write a client now.
- The existence of schematic upload, rendering and "simulation evidence" tables suggests the Squid project is moving toward machine-verified submissions — a natural interoperability target for an automated door benchmark.
- The Squid bot's configuration key formerly named `SYNERGY_SECRET` indicates an integration between the bot and the Synergy server.

### Gaps
- Public base URL of the Squid API / web catalogue not found (repo uses `api.example` / `frontend.example` placeholders). Live record list therefore unverified.
- No "Piston Door Catalog(ue)" spreadsheet, "Redstone Records" Discord, Storage Tech door list, or "Smallest Observerless" list could be located by web search; they may exist only inside Discord.
- techmc.wiki / Storage Tech docs were not found to contain door records.

---

## 5. Current smallest-volume (and fastest) records for 3×3 … 7×7 and larger, Java Edition

### Takeaway
As of late 2026 the headline Java "smallest seamless" figures found are: 3×3 = 55 (5×11×1), 4×4 = 99 (9×1×11), 5×5 ≈ 200–209 (already labelled "former"; current value not found), 6×6 = 308 published but superseded by an unpublished sub-247 design, 7×7 = 360 (1×24×15). All of these are 1-wide, entity-laden, version-fragile and extremely slow (6×6/7×7 take over an hour to open). Entity-free or practical-speed doors are 1.3×–10× larger.

### Cited Findings
**Smallest (unrestricted; entities allowed) — all Java Edition, self-reported by builders**

| Opening | Volume | Dimensions | Creators | Completed | Notes | Source |
|---|---|---|---|---|---|---|
| 2×2 | 24 | n/a | unknown (design possible since 13w09b, Feb 2013) | 2013 | Stood until 2025 | [Wiki Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses), [2x2 doc](https://docs.google.com/document/d/1iz1zYdcQJZ3_MFN8fElV-kCd8cratsy37Q68PvKY3BI/edit) |
| 2×2 | < 24 (figure not found) | n/a | Door_Maker, Ganymede | 31 May 2025 (posted 17 Jun 2025) | 1.21.6 snapshot lead mechanics; bee/cat minecarts, chicken, shulker | [2x2 doc](https://docs.google.com/document/d/1iz1zYdcQJZ3_MFN8fElV-kCd8cratsy37Q68PvKY3BI/edit), [Kawediloru](https://www.youtube.com/watch?v=LIEjoeGg5pQ) |
| 3×3 | 55 | 5×11×1 | Ganymede, Door_Maker, SacredRedstone, Br1ckcraft3r | 11 Jul 2025 (V1); V2 23 Aug 2026; V3 25 Aug 2026 | V1: 22 entities, 1.8 s close / 1.95 s open, not loc/dir, 1.17–1.21.10 (broke in 1.21.11 when NaN carts were removed). V2: 11 entities, 1.16–26.3+, locational, breaks on Paper. | [Br1ckcraft3r](https://www.youtube.com/watch?v=N_yOjRYGA_w), [Door_Maker](https://www.youtube.com/watch?v=dxcZcYBB75s), [Kawediloru](https://www.youtube.com/watch?v=y2MondmQWQo) |
| 3×3 (no entities) | 56 | 7×8×1 | SacredRedstone | 22 May 2017 | Record 2017–2025; seamless, entityless | [SacredRedstone](https://www.youtube.com/watch?v=rH34dMlb1Q8), [Wiki](https://minecraft.wiki/w/Tutorial:Piston_uses) |
| 4×4 | 99 | 9×1×11 | Door_Maker, Cwee, Excert (+LEOPAUL59) | v1 16 Sep 2023; v2 3 Nov 2023; v5 26 Aug 2024 | Builders claim it cannot be beaten; does not work on Paper; later versions use NaN minecarts / frozen fireball | [Cwee](https://www.youtube.com/watch?v=AUVLmzOYXFU), [4x4 doc](https://docs.google.com/document/d/1iO0H9vkPXjHwVsbbhnfFPcMnK3TP_SGNZtRMAiXsSSU/edit) |
| 4×4 (prev.) | 108 | n/a | Door_Maker, Cwee, Wilux, Arway, HiHi | Dec 2022 | 1 mob + other entities, not loc/dir | [Cwee](https://www.youtube.com/watch?v=Fd-p6AA3syg) |
| 4×4 (slimeless, pre-entity era) | 112 | n/a | MegaTech (matching MDP's 112 with slime, Oct 2017) | 22 Jan 2018 | Stood ~5 years | [4x4 doc](https://docs.google.com/document/d/1iO0H9vkPXjHwVsbbhnfFPcMnK3TP_SGNZtRMAiXsSSU/edit) |
| 4×4 funnel/vault | 140 | 10×7×2 | Door_Maker | Aug 2025 | 26 entities, 100% dense, 1.21.6–1.21.10; previous long-standing vault record 160 by abh037 (2014–2023) | [Door_Maker](https://www.youtube.com/watch?v=zZaE-SkJFp4), [Wiki](https://minecraft.wiki/w/Tutorial:Piston_uses) |
| 5×5 | 209 ("former") | n/a | Door_Maker, Cwee957, Arway | posted 25 Jul 2023 | ~3 s close, ~3 min 08 s open; 20 entities incl. 4 mobs; 1.19.4+ (jukebox) | [Cwee](https://www.youtube.com/watch?v=Vnufu6Het5M) |
| 5×5 carpet (seamless carpet hallway) | 200 | 20×1×10 | Cwee, Door_Maker, Arway | 28 Sep 2023 | 15 entities; beat prior carpet record by 28; 1.19.4+ | [Cwee](https://www.youtube.com/watch?v=oCPP8LWJyXY) |
| 5×5 (earlier) | 220 | n/a | Cwee, Arway, Door_Maker, HiHi et al. | Jul 2022 | 5 min open (predecessor 228 blocks took 17 min) | [Cwee](https://www.youtube.com/watch?v=UF-QA5weAEY) |
| 5×5 glass | 312 | 1×13×24 | Door_Maker, Cwee957 | 13 Jul 2025 | 31 entities; ~9 s close, ~1 h 9 min open; 1.21.6+ | [Cwee](https://www.youtube.com/watch?v=bElDoe5wcaQ) |
| 6×6 | 308 ("former") | 1×22×14 | Door_Maker, Cwee957 (BE layout by wuwuwuwullll) | 22 Jun 2025 | 71 entities; ~9 s close, ~1 h 20 min open; 1.21+; beat 322, and Davidjohn66's 420. Description says Door_Maker has since posted a 247-block design and that even that is not the record. | [Cwee](https://www.youtube.com/watch?v=1Ojxa1Ljj_8) |
| 6×6 (earlier) | 338 | n/a | Door_Maker, Arway, Cwee | 2022 (video Aug 2023) | 84 entities; ~7.5 min open | [Cwee](https://www.youtube.com/watch?v=6COWu8vCras) |
| 6×6 no entities | 360 | 1×24×15 | Door_Maker, Cwee957 | 9 Aug 2025 | ~1 min 12 s close, ~1 h 34 min open; 1.21+; runs on a clock | [Cwee](https://www.youtube.com/watch?v=VZhG8DUL2L8) |
| 7×7 | 360 | 1×24×15 | Door_Maker, Cwee957 | 23 Jun 2025 | 75 entities; ~10 s close, ~1 h 47 min open; 1.21.6+; beat 375, Davidjohn66's 506 and PixieBlox's 484 | [Cwee](https://www.youtube.com/watch?v=ipAx9-AOng4) |
| 7×7 "cycleless" (practical-ish) | 484 | 11×2×22 | PixieBlox | Mar 2025 | ~3 s close, ~33 s open; 1.16.0–1.21.9 | [PixieBlox](https://www.youtube.com/watch?v=Y4N6ra8z0hE) |
| 8×8 "cycleless" | 576 | 12×2×23 | PixieBlox | by Mar 2026 | "Was the smallest at some point"; 1.15–1.21.9; unreliable per author | [PixieBlox](https://www.youtube.com/watch?v=peN5BqEV768) |
| 9×9 | 476 | 1×28×17 | Door_Maker, Cwee957 | 24 Jun 2025 | 79 entities; ~12 s close, ~2 h 55 min open; beat 493, Davidjohn66's 728 | [Cwee](https://www.youtube.com/watch?v=yxkHhoNJGso) |
| 9×9 no entities | 540 | 1×30×18 | Door_Maker, Cwee957 | 6 Aug 2025 | 1.21+ | [Cwee](https://www.youtube.com/watch?v=HeiOLupsVXg) |
| 10×10 | 608 | 1×32×19 | Door_Maker, Cwee957 | 16 Jan 2024 | 55 entities; 3 min 13 s close, ~4 h 15 min open; beat 840 and Davidjohn66's 868 | [Cwee](https://www.youtube.com/watch?v=YaC0OOCgeUU) |

**Entity-free / restricted and practical-speed reference points**
- 3×3: 72 blocks (8×9×1), 0.6 s open / 0.7 s close — "smallest 0.6 s 3×3" by avogaado, JensundLars, lum3nd0, PixieBlox (Feb 2023). — [JensundLars](https://www.youtube.com/watch?v=R6e__lLvwrg), [avogaado](https://www.youtube.com/watch?v=jKqjZdTyW4E)
- 3×3 history: 2730 (2011) → 210 → 140 (first 1-wide, 2012) → 96 (2013) → 63 (JeffreyZhu, Nov 2016) → 56 (Sep 2017) → 55 (Jul 2025). — [Purplers door list](https://docs.google.com/document/d/1MOT4I41A1mFjLGfK19F5cwNPYSLizsQrUytsIMnnHfM/edit)
- 4×4: 132 blocks (12×11, i.e. 1 wide), no entities, contained, 0.9 s open / 0.95 s close, Java 1.19+, by Br1ckcraft3r and Door_Maker, completed 20 Feb 2026 ("fastest 132b" / smallest 0.9 s 4×4). — [Br1ckcraft3r](https://www.youtube.com/watch?v=LKFnjR6V-a8)
- 4×4: 168 blocks seamless, tileable, 1-wide (avogaado); 180 blocks "super sync" (Sidney600MC and G4me4u, Dec 2016, first observer-era record); 308 blocks fully sync, 0.4 s open / 0.3 s close. — [Wiki](https://minecraft.wiki/w/Tutorial:Piston_uses), [4x4 doc](https://docs.google.com/document/d/1iO0H9vkPXjHwVsbbhnfFPcMnK3TP_SGNZtRMAiXsSSU/edit), [Ya boi immense lad](https://www.youtube.com/watch?v=5tWmnXiCqxY)
- 5×5: 504 blocks, entityless and observerless (WolfieNamira, Oct 2022); wiki lists a 504-block seamless 5×5 with 1.95 s opening. — [WolfieNamira](https://www.youtube.com/watch?v=8z25R3CFBUo), [Wiki](https://minecraft.wiki/w/Tutorial:Piston_uses)
- 5×5: 540 blocks (18×2×15), seamless + slimeless, 1 s open / 1.25 s close, 3 entities, Java 1.21+ (Br1ckcraft3r, 9 Feb 2026). 5×5: 715 blocks (13×5×11), no entities, no slime/honey, 0.85 s open / 0.6 s close, Java 1.16+ (backslash7 and Br1ckcraft3r, Apr–May 2026). — [540b](https://www.youtube.com/watch?v=qKYv33Rt71s), [715b](https://www.youtube.com/watch?v=eVy2hLuMiSg)
- 5×5 tutorial-grade: 576 blocks (CraftyMasterman, ~2020); "best 5×5" 780 blocks (13×12×5) at 0.9 s open (2023). — [CraftyMasterman](https://www.youtube.com/watch?v=iCCjbzZUj-4), [avogaado](https://www.youtube.com/watch?v=jKqjZdTyW4E)
- 6×6 older practical records: 1260 blocks (2013), 950 blocks (2014), 900 (10×18×5, ~2019). — YouTube titles: [Sidney600MC](https://www.youtube.com/watch?v=s5XWfCDxlso), [Mrbillybobcorndog](https://www.youtube.com/watch?v=NITQZ8NSIzc), [Armadillo28](https://www.youtube.com/watch?v=yQZphBMbL7g)
- 7×7 practical: 1540 blocks observerless (Frozen Whiskers, ~2025); 1824 blocks at 1.95 s open (Algi, ~2023); hobbyist server build 4940 blocks at 1.6 s open (Oct 2025). — [Frozen Whiskers](https://www.youtube.com/watch?v=rpIrWeAHKu8), [Algi](https://www.youtube.com/watch?v=74Fsn5mgRkQ), [redstone-server.info](https://redstone-server.info/node/12079)
- 8×8 observerless 1932 (12×23×7); 9×9 2268 (sammyuri, ~2021); 10×10 observerless 2520 (Armadillo28, Feb 2020; broken by 1.16 dust changes). — [Armadillo28 8x8](https://www.youtube.com/watch?v=312-znHiU0Q), [sammyuri](https://www.youtube.com/watch?v=JYjgiUp5VXE), [Armadillo28 10x10](https://www.youtube.com/watch?v=8Kgx14przLE)

**Fastest**
- 3×3: instant close, 0.25 s open (0.4 s seamless), 396 blocks (18×2×11), Br1ckcraft3r, 1 May 2025, Java 1.16+; a 360-block variant with more reset exists. Earlier "best 3×3": 0.3 s open/close, 300 blocks (10×10×3), lum3nd0. — [Br1ckcraft3r](https://www.youtube.com/watch?v=lc2BykI7o2k), [avogaado](https://www.youtube.com/watch?v=jKqjZdTyW4E)
- 4×4: 0.4 s open / 0.3 s close in 308 blocks (smallest at that speed); Dico's 2014 "fastest possible" 4×4 opened in 0.15 s using large-scale 0-ticks; a later "smaller fastest possible" build is 4032 blocks. — [Ya boi immense lad](https://www.youtube.com/watch?v=5tWmnXiCqxY), [4x4 doc](https://docs.google.com/document/d/1iO0H9vkPXjHwVsbbhnfFPcMnK3TP_SGNZtRMAiXsSSU/edit), [BenoRedstoner](https://www.youtube.com/watch?v=NCvmjoxgHHY)
- 5×5: 0.4 s open and close (0.45 s for middle blocks), 22×24×25 = 13,200 blocks, Timmerman and lum3nd0, finished 22 Feb 2025, Java 1.21+ only, contained, fully reliable. — [lum3nd0](https://www.youtube.com/watch?v=ZPM5FpnGhtA)
- 6×6: 0.4 s open and close, 704 blocks, unseamless, 0-reset (avogaado, StevesCrafts). — [Wiki](https://minecraft.wiki/w/Tutorial:Piston_uses)
- 7×7: 0.85 s open and close, 26,796 blocks (JensundLars, maganiso, Sirrcacti; Apr 2026). — [JensundLars](https://www.youtube.com/watch?v=_ZxRhmW-YJg)

**Bedrock (for contrast)**
- Bedrock has separate records, e.g. a 63-block 3×3 (2020), "smallest 7×7 … only 1 wide" and fastest 10×10 at 6.6 s open (ElcTest); the Java 1-wide 6×6–10×10 records reuse a Bedrock layout by wuwuwuwullll. — [Seishin Rimu](https://www.youtube.com/watch?v=gwKM2PeVHys), [ElcTest](https://www.youtube.com/watch?v=HyaqYG1ZOX0), [Cwee 7x7](https://www.youtube.com/watch?v=ipAx9-AOng4)

### Inferences
- Unrestricted smallest volume grows far more slowly than opening area: 55 → 99 → ~200 → ≤247–308 → 360 for 3×3 … 7×7 (7×7 is ~6.5× the 3×3 volume for 5.4× the area), because 1-wide "worm/tape" layouts trade time for space. Speed collapses instead: ~2 s (3×3) → minutes (5×5) → 1–2 hours (6×6, 7×7).
- For an LLM-agent benchmark that needs fast, deterministic, entity-free doors, more appropriate human baselines are: 3×3 = 56 (entityless) or 72 (0.6 s); 4×4 = 112 (slimeless, 2018) or 132 (entityless, 0.9 s); 5×5 = 504 (entityless + observerless) / 540 / 715; 6×6 = 360 (entityless but ~1.5 h) or ~900–950 (practical); 7×7 = 484 (cycleless, 33 s) or ~1540–1824 (practical).
- The 6×6 "308" and 5×5 "209/200" are explicitly flagged as former records; the true current figures are held on Squid/Synergy and unpublished on YouTube as of my searches.

### Gaps
- Current smallest 5×5 regular record (successor to 209) — not found.
- Current smallest 6×6 record (description says < 247) — figure, date, and source not found.
- Volume of the 2025 sub-24 2×2 — not stated in the sources read.
- Whether 99 is still the 4×4 record in Nov 2026 — not independently confirmed (no later claim found).
- Flush / hipster / trapdoor-category smallest records for each size — not found on the open web.
- None of the above was verified against the Squid #record-logs; all are builder self-reports. Wiki notes the 55-block 3×3 "involves multiple entities" which corroborates only that one.

---

## 6. Which game mechanics do compact doors rely on; Java vs Bedrock; changes across Java versions; locational/directional behaviour

### Takeaway
Record doors are Java-only because they depend on Java-specific behaviour: quasi-connectivity, sticky pistons dropping blocks on short pulses, deterministic sub-tick ordering (tile-tick priorities, block events) that enables 0-ticks, and — for the smallest records since 2022 — entity exploits (minecart stacks, NaN-motion carts, frozen fireballs, non-ticking entities). These are fragile: individual records list narrow version windows and several broke in 1.16, 1.21.10 and 1.21.11.

### Cited Findings
**Core piston facts**
- Push limit: a piston moves at most 12 blocks; Mojang has said the limit is by design. — [Wiki Piston](https://minecraft.wiki/w/Piston)
- Java timing: start delay 0 gt if powered in the scheduled-tick / random-tick / block-event phase, 1 gt if powered by player input or in the entity / block-entity phase; extension and retraction each take 2 gt; chained pistons pushing redstone blocks fire 3 gt apart. A Java piston de-powered mid-extension aborts while the pushed blocks carry on. — [Wiki Piston](https://minecraft.wiki/w/Piston)
- Bedrock timing: fixed 2 gt start delay, activation only on a "consume" tick; extension/retraction 2 gt. — [Wiki Piston](https://minecraft.wiki/w/Piston)
- Slime/honey: adjacent blocks move with a pushed sticky block; slime and honey do not stick to each other; glazed terracotta does not stick; an immovable block in the group prevents the move. — [Wiki Piston](https://minecraft.wiki/w/Piston)

**Java-only mechanics**
- Quasi-connectivity: pistons, dispensers and droppers can be activated by anything that would power the space above them; officially "works as intended" (MC-108); crafters are not affected. Two forms: immediate QC (dust, torches, repeaters, levers etc. also update the piston) and update-based QC (piston is powered but waits for a block update → BUD behaviour). The wiki tutorial is scoped to Java and Legacy Console only. — [Wiki QC tutorial](https://minecraft.wiki/w/Tutorial:Quasi-connectivity)
- On Bedrock, QC is absent (its role replaced by observers). — [Wiki Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses), [Wiki Parity issue list](https://minecraft.wiki/w/Parity_issue_list)
- Block dropping: on Java a sticky piston given a 1-tick pulse leaves its block behind; on Bedrock it retracts the block. — [Wiki Parity issue list](https://minecraft.wiki/w/Parity_issue_list)
- 0-tick pulses: a signal that turns on and off within one game tick, made by powering a line and removing the source with a piston later in the same tick (via tile-tick priorities or budded pistons); sticky pistons then drop their block and retract instantly. Relies on tile ticks (repeaters, then comparators) being processed before block events. Tutorial is Java / Legacy Console only, and warns such behaviour may be patched. — [Wiki Zero-ticking](https://minecraft.wiki/w/Tutorial:Zero-ticking)
- Many of the faster doors use Java-only zero-tick techniques. — [Wiki Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses)
- Bedrock transmits redstone power in a random order (listed as a parity difference); Bedrock flying machines are more restricted for lack of QC and block dropping. — [Wiki Parity issue list](https://minecraft.wiki/w/Parity_issue_list), [Wiki Flying machines](https://minecraft.wiki/w/Tutorial:Flying_machines)
- Player input vs repeater input differ in Java (MC-172213), which is why the rules require both and builders flag doors as "input bugged" or needing repeater input. — [Squid Rules §3.1](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md), [Cwee 99b 4x4](https://www.youtube.com/watch?v=AUVLmzOYXFU)
- Observer tile-tick priority is cited by record builders as a hard constraint on layouts (reason given for the 99-block 4×4 being unbeatable). — [Cwee 99b 4x4](https://www.youtube.com/watch?v=AUVLmzOYXFU)

**Version history relevant to doors (Java)**
- 1.3.1 (12w26a): pistons schedule extensions/retractions instead of executing immediately. 1.5 (13 Mar 2013): the "Redstone Update" (droppers among the additions; redstone-block sliders appear in 4×4 doors within weeks); a 288-block 4×4 record broke at 1.5. — [Wiki Piston](https://minecraft.wiki/w/Piston), [4x4 doc](https://docs.google.com/document/d/1iO0H9vkPXjHwVsbbhnfFPcMnK3TP_SGNZtRMAiXsSSU/edit)
- 1.8 (14w18a, Apr 2014): slime blocks become sticky. 1.11 (Nov 2016): observers added to Java (Bedrock/MCPE had pistons and observers from 0.15.0, Jun 2016); first observer-based 4×4 record Dec 2016. — [Wiki Piston](https://minecraft.wiki/w/Piston), [4x4 doc](https://docs.google.com/document/d/1iO0H9vkPXjHwVsbbhnfFPcMnK3TP_SGNZtRMAiXsSSU/edit)
- 1.13 pre7: regular pistons briefly gained sticky-piston block-dropping; removed in 1.13.1. 1.15 (19w41a): honey blocks. 1.16 (20w06a): pistons no longer pop components off their back when retracting; 1.16 redstone-dust changes broke at least one record door (2520-block 10×10). — [Wiki Piston](https://minecraft.wiki/w/Piston), [Armadillo28](https://www.youtube.com/watch?v=8Kgx14przLE)
- Version floors quoted on records: 1.16+ (many fast doors), 1.19+ (132-block 4×4), 1.19.4+ (jukebox-as-timer in 5×5 records), 1.21+ (copper bulbs; new disc lengths, "creator" disc), 1.21.6+ (lead mechanics, creaking rename, minecart memory-leak fix). — [Br1ckcraft3r](https://www.youtube.com/watch?v=LKFnjR6V-a8), [Cwee 5x5](https://www.youtube.com/watch?v=Vnufu6Het5M), [lum3nd0](https://www.youtube.com/watch?v=ZPM5FpnGhtA), [Cwee 6x6](https://www.youtube.com/watch?v=1Ojxa1Ljj_8), [Cwee 7x7](https://www.youtube.com/watch?v=ipAx9-AOng4)
- Breakages: NaN minecarts were patched in snapshot 25w45a (1.21.11), breaking the 55-block 3×3 V1; PixieBlox's 7×7/8×8 broke in 1.21.10 and the 7×7 opening became far slower in 1.21.11. — [Door_Maker](https://www.youtube.com/watch?v=dxcZcYBB75s), [PixieBlox 7x7](https://www.youtube.com/watch?v=Y4N6ra8z0hE), [PixieBlox 8x8](https://www.youtube.com/watch?v=peN5BqEV768)
- Redstone Experiments (experimental data pack, added 24w33a / 1.21.2, Aug 2024; still listed as a current experiment with latest release 26.3): aims to make redstone wire behave the same regardless of position and orientation; update order is derived from signal direction, with ties randomised; wire sets all connected strengths before emitting neighbour updates, only updates blocks it can power, and no longer reacts to other wires' updates. Off by default. — [Wiki Redstone Experiments](https://minecraft.wiki/w/Redstone_Experiments)
- Java release numbering has moved to year-based versions (26.1, 26.3 current, 26.4 upcoming). — [Wiki Redstone Experiments](https://minecraft.wiki/w/Redstone_Experiments), [Br1ckcraft3r](https://www.youtube.com/watch?v=N_yOjRYGA_w)

**Entity tech in size records**
- Techniques named by builders: mobs/minecarts moved by pistons to power inputs in awkward spots; non-ticking entities (hard to obtain); NaN minecarts (broken motion values, float in place, only pistons move them); frozen/stationary dragon fireballs and wither skulls; furnace/chest/hopper minecart stacks; jukebox disc lengths as long timers; armor stands; shulkers; allays. — [4x4 doc](https://docs.google.com/document/d/1iO0H9vkPXjHwVsbbhnfFPcMnK3TP_SGNZtRMAiXsSSU/edit), [Cwee 5x5 carpet](https://www.youtube.com/watch?v=oCPP8LWJyXY), [Door_Maker 3x3](https://www.youtube.com/watch?v=dxcZcYBB75s), [Cwee 7x7](https://www.youtube.com/watch?v=ipAx9-AOng4)
- Entity-dependent doors are sensitive to entity ticking order and to server software: several "break on Paper servers", one "can break on Paper due to ticking order being shuffled on reload", and V2/V3 of the 55-block 3×3 are locational because entities must share a sub-chunk. — [Door_Maker](https://www.youtube.com/watch?v=dxcZcYBB75s), [Br1ckcraft3r](https://www.youtube.com/watch?v=N_yOjRYGA_w), [Cwee](https://www.youtube.com/watch?v=AUVLmzOYXFU)

**Locational / directional**
- Wiki definitions: locational = works only at certain coordinates (chunk-border effects); directional = works only in one orientation. — [Wiki Piston uses](https://minecraft.wiki/w/Tutorial:Piston_uses)
- Records advertise "not locational and not directional" as a feature, and fastest doors credit helpers for "loc and reset fixes" — i.e. locationality is a common defect that must be engineered out. — [Cwee 108b 4x4](https://www.youtube.com/watch?v=Fd-p6AA3syg), [lum3nd0](https://www.youtube.com/watch?v=ZPM5FpnGhtA)
- Analysis tooling used by top builders: G4mespeed, Capture & Playback, Block Event Separator, Carpet mod. — [lum3nd0](https://www.youtube.com/watch?v=ZPM5FpnGhtA), [Purplers](https://www.youtube.com/watch?v=5cYDoWDI7Dw), [Armadillo28](https://www.youtube.com/watch?v=8Kgx14przLE)

### Inferences
- A benchmark must pin one exact Java version and server implementation (vanilla, not Paper) and state whether Redstone Experiments is off (default); human baselines are only comparable inside each record's stated version window.
- Simple, slower doors built from dust/repeaters/sticky pistons with QC but no 0-ticks or entities are the most version-stable class; that is the regime where entity-free baselines (56 / 112–132 / 504–715) apply.
- Locationality in non-entity doors typically comes from redstone-dust update order and block-event ordering; the experimental redstone changes target the dust part but would themselves alter timing of existing doors. (The wiki states the design aim; specific door breakage is my inference.)

### Gaps
- No wiki-sourced statement was retrieved for target blocks, note blocks, powered rails or copper bulbs as door components (only builder mentions of copper-bulb sounds and jukeboxes). Their roles (target = dust redirection; note block / powered rail as compact QC/BUD-updatable components; copper bulb as 1-tick T-flip-flop) are common knowledge in the community but unsourced here.
- Bedrock movable block entities (pushing chests/hoppers etc.) and Bedrock's lack of 0-ticks were not confirmed by a fetched source.
- Exact details of the 1.16 dust change and whether the 1.21.2 experiment has been promoted to default in any 26.x release were not confirmed beyond the wiki listing it as still experimental.

---

## 7. Why is the jump from 3×3 to larger doors so steep; largest doors built; typical size/complexity of 5×5–7×7

### Takeaway
A 3×3 can be cleared with double piston extenders around a small frame, but each size step needs longer multi-piston extenders whose retraction must be sequenced one block at a time, and at 6×6+ a single column of door blocks plus machinery runs into the 12-block push limit. Practical (seconds-scale, entity-free) doors run roughly 500–800 blocks at 5×5, ~700–1300 at 6×6 and ~1500–5000 at 7×7; speed-record doors reach 13,000–27,000 blocks.

### Cited Findings
- Push limit of 12 blocks per piston, by design. — [Wiki Piston](https://minecraft.wiki/w/Piston)
- Concrete push-limit collision at 6×6: in a 2026 redstone-block-frame 6×6, the bottom piston pushes exactly 12 blocks (1 piston + 6 sand + 5 redstone blocks), which forces a design compromise (hallway not continuable). — [Cwee, Aug 2026](https://www.youtube.com/watch?v=iD6u2gJwWM0)
- Vocabulary of large-door parts in builder notes: double/"quint" (5-long) extenders, "side double extender", "top slider" with "pushback", "piston tape", "worm", "fold sliders", clocks driving tapes, timers of 25 items, jukebox discs as timers. — [Cwee 5x5 carpet](https://www.youtube.com/watch?v=oCPP8LWJyXY), [Cwee 4x4](https://www.youtube.com/watch?v=AUVLmzOYXFU), [Cwee Aug 2026](https://www.youtube.com/watch?v=iD6u2gJwWM0)
- Community view that double piston extenders and being seamless-when-open are what characterise a 3×3. — [r/redstone thread mirror](https://axebps-redlib.hf.space/r/redstone/comments/1jb1g23/3x3_extremely_fast_automatic_open_and_shut) (forum comment)
- Effort scale: 5×5 220-block record took 10 months; 5×5 200-block needed ~10 h just to tune one clock; 6×6 338-block took about a year; 540-block 1 s 5×5 took almost two years; fastest 5×5 took 3 months. — [Cwee 220](https://www.youtube.com/watch?v=UF-QA5weAEY), [Cwee 200](https://www.youtube.com/watch?v=oCPP8LWJyXY), [Cwee 338](https://www.youtube.com/watch?v=6COWu8vCras), [Br1ckcraft3r](https://www.youtube.com/watch?v=qKYv33Rt71s), [lum3nd0](https://www.youtube.com/watch?v=ZPM5FpnGhtA)
- Volume/speed trade-off at fixed size (5×5): 200–209 blocks at ~3 min open; 504 at 1.95 s; 540 at 1 s; 715 at 0.85 s; 780 at 0.9 s (2023); 13,200 at 0.4 s. — sources in section 5
- 7×7: 360 blocks at ~1 h 47 min; 484 at ~33 s; 1824 at 1.95 s; 4940 at 1.6 s (hobbyist); 26,796 at 0.85 s. — sources in section 5
- Entity counts in minimal big doors: 71 (6×6), 75 (7×7), 79 (9×9), 55 (10×10). — [Cwee 6x6](https://www.youtube.com/watch?v=1Ojxa1Ljj_8), [7x7](https://www.youtube.com/watch?v=ipAx9-AOng4), [9x9](https://www.youtube.com/watch?v=yxkHhoNJGso), [10x10](https://www.youtube.com/watch?v=YaC0OOCgeUU)
- Largest doors: Lord Jon25's 384×384 piston door (flying-machine based, built in 1.18 snapshot 21w14a, Apr 2021; successor to a 256×256), billed as the biggest possible at the 1.18 world height. Largest without flying machines claimed in Nov 2021: a 17×17 cave door (viscosealt). The first 10×10 dates to ~2013 (Freya). A wiki-listed "scalable" design goes up to 15×7. avogaado published "Building Minecraft's LARGEST Piston Door" in Jul 2026 (size not in description). — [Lord Jon25](https://www.youtube.com/watch?v=qZUO8K9ohGw), [viscosealt](https://www.youtube.com/watch?v=vF16fSRFpK4), [Freya](https://www.youtube.com/watch?v=__saywoX7g4), [Wiki](https://minecraft.wiki/w/Tutorial:Piston_uses), [avogaado](https://www.youtube.com/watch?v=YkMhE7cxveM)
- Squid rules recognise NO FLYING MACHINES as a restriction and define a flying machine as a block unit using an internal loop to move itself multiple blocks. — [Squid Rules §2.1.6](https://github.com/redstone-squid/Redstone-Squid/blob/master/reference/Door_Rules.md)

### Inferences
- Geometric driver: in a regular seamless N×N door every door block must leave the frame along a row or column, so the deepest blocks need an extender of reach ≈ ⌈N/2⌉ from the sides or up to N from one side; an n-long piston extender needs O(n) pistons but O(n²)-ish sequenced pulses to retract, so control logic (not the pistons) dominates volume and time. 2×2 needs single pistons, 3×3 doubles/triples, 5×5 already uses quintuple extenders in 1-wide layouts.
- At 6×6 and up, a stack of N door blocks plus the extender's own pistons approaches 12 pushed blocks, so designers must split columns, use slime/honey "worms", or feed blocks through "tapes" — which is why 1-wide minimal doors become hour-long sequential machines.
- For benchmark difficulty calibration: 3×3 is a solved, tutorial-level task (56–72 blocks, hundreds of public tutorials); 4×4 is intermediate (99–180); 5×5 is where sequencing logic becomes the bulk of the build (≥ 500 blocks entity-free); 6×6–7×7 entity-free doors at seconds-scale speed are expert-team projects taking months. An LLM agent producing any working seamless 5×5 would be a meaningful result; matching 504–715 would be expert-level.
- Flying-machine doors scale almost without limit (384×384) but are a different category from piston-layout doors and are slow/uncontained; the largest "true layout" doors that are regularly optimised are 10×10 (608 minimal; 2520 observerless practical).

### Gaps
- No source gives piston/component counts for 5×5–7×7 doors; only volumes and entity counts were found.
- No authoritative statement of the minimum extender length per door size was found; the geometric argument above is my own inference.
- Size of avogaado's 2026 "largest piston door" and any 2022+ successor to the 384×384 were not retrieved.
- "Largest non-flying-machine door" (17×17, 2021) is a single self-claim and may have been surpassed.
