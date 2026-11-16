# Piston-door repair and physics-adaptation tasks

Each task hands the agent a broken or mis-tuned piston door built from one of the agents' own
verified doors (`runs/bench/dashboard/runs.json`, status "door"). The agent must return a door
that passes. The checker is the existing grader: `grade(kernel, design, n, "seamless", "final")`
under the task's physics, plus the task's constraints.

## Folder

| Path | What it is |
|---|---|
| `tasks/<id>.json` | one task per file (format below) |
| `check.py` | grades a submission for a task; enforces the constraints and refuses hacks |
| `lib.py` | shared helpers: kernel boot (1G heap, temp dirs in `/private/tmp/claude-501/tasks_doors_k`), edit distance, the census neighbourhood generalised to rectangular doors, screen/dev/final grading ladder |
| `gen_matrix.py` | grades every verified door (volume ≤ 1500) under 9 physics settings → `data/physics_matrix.json` |
| `gen_repair.py` | repair tasks: k = 2–4 perturbations + single-edit brute force |
| `gen_port.py`, `make_ports.sh` | port and hidden-rule tasks from the physics matrix |
| `make_repairs.sh` | the repair-generation commands that produced the current set |
| `verify_tasks.py` | re-checks every task with `check.py`: start must fail, reference must pass (final grade), hack probes must be refused; writes the `verified` field |
| `data/` | small bookkeeping: physics matrix, per-door repair attempts (including rejected perturbations and the single edit that fixed them), per-port search logs |
| `logs/` | generator stdout |
| `SUMMARY.md` | the task table with difficulty stats |

## Task format

```jsonc
{
  "id": "repair-3x3-w1-fable-a-k3",
  "family": "piston_doors",
  "kind": "repair" | "port" | "hidden_rule",
  "n": 3,                       // grader size: an int (square) or [w, h]; passed to grade() as-is
  "size": "3x3",
  "track": "seamless",          // always the seamless track
  "physics": {},                // grading physics for the Kernel; {} = vanilla 26.3
  "physics_told": true,         // false for hidden_rule: do not show "physics" to the agent
  "told": "...",                // the task statement shown to the agent (with "start")
  "start": {"initial_state": "open", "blocks": [...]},   // candidate format, as in result.json
  "constraints": {
    "max_volume": 70,           // measured swept box volume (grader's "volume") must be <= this
    "max_blocks": null,         // optional block budget (blocks excluding lever and doorway)
    "allowed_blocks": null,     // optional list of block ids; null = the rulebook allow-list
    "edit_budget": 5,           // optional: max cells that may differ from "start" (repair only)
    "initial_state": "open"     // optional: required initial_state (repair only)
  },
  "reference": {                // a known solution, confirmed to pass with the final grade
    "source": "w1-fable-a", "kind": "original door" | "another agent's door" | "retimed start door",
    "design": {...}, "volume": 70, "open_ticks": 34, "close_ticks": 22, "edits_from_start": 3
  },
  "provenance": {...},          // seed run, perturbation edits / home physics, generator
  "difficulty": {
    "single_edit_fix": false,   // true / false (full brute force) / "none found (partial search)"
    "neighbourhood_size": 3416, // census neighbourhood of "start" (57 block states per cell of its box)
    "neighbours_graded": 3416,
    "brute_force": "full",      // or a description of the partial search
    "edits_made": 3,            // repair: k
    "same_volume_port_known": true,   // port / hidden_rule
    "start_fail": "did_not_open", "start_final_partial": 0.0,
    "reference_volume": 70, "reference_open_ticks": 34, "reference_close_ticks": 22
  },
  "verified": {...}             // written by verify_tasks.py: start fails, reference passes, hacks refused
}
```

What the agent sees: `told`, `start`, `size`/`n`, `constraints`, and `physics` only when
`physics_told` is true. Everything else is grader-side.

## Checking a submission

```
python3 check.py tasks/<id>.json submission.json                # final grade (8 cycles); exit 0 = pass
python3 check.py tasks/<id>.json submission.json --mode dev     # 3-cycle dev grade, for quick iteration
```

`check(task, design, kernel=None, mode="final")` is the Python entry point; pass a kernel
started with the task's physics to grade many submissions without rebooting.

A submission passes when all of these hold:

1. **Format and rulebook.** `validate(design, task.n)`: allow-list, one lever, doorway cells hold
   only stone, empty hallway, no hallway-wall cells, consistent piston heads.
2. **Size is the task's.** The task's `n` is always used. A submission that states a different
   `n`/`size` is refused, so the doorway cannot be moved or resized.
3. **Static constraints**, before any simulation: allowed blocks, block budget, the placed blocks'
   bounding box (with the doorway) must already fit in `max_volume`, `initial_state` if fixed,
   and the edit budget (cells whose normalised block differs from `start`; wire shape/power,
   `powered`, `lit`, `extended` are ignored; a changed `initial_state` counts as one edit).
4. **The grader's verdict.** `grade(kernel, design, n, "seamless", "final")` under the task's
   physics must be valid. The grader already refuses a removed door (the doorway must
   reach all-stone and all-air on every flip), blocks in the hallway, moved wall blocks,
   entities and non-plain blocks visible beside the open doorway.
5. **Measured volume** (`grade()["volume"]`, the swept box) `<= max_volume`.

Physics is fixed by the task. Anything the submission says about physics is ignored.

## How tasks were made and verified

**Repair** (`gen_repair.py`). Start from a verified door under its own physics. Draw k "natural"
edits at cells at least two apart: wrong facing, wrong repeater delay, sticky ↔ normal piston,
slime ↔ honey, a block swapped for glass/stone/obsidian, a deleted block. Each edit must break
the door on its own (1-cycle screen). The combined design must fail. Then every single edit in
the census neighbourhood of the perturbed design (the 57 census block states at every cell of
its bounding box except doorway, hallway, walls and lever), plus each exact revert, is graded.
Any edit that passes the final grade rejects the perturbation. Neighbourhoods above 4,200 edits
(the 4×4 doors) get a partial search instead: every state at and next to the perturbed cells, the
exact reverts, and a random sample of 1,200 of the rest; those tasks say so in `brute_force`.

**Port** (`gen_port.py`). `gen_matrix.py` grades every door under 9 physics settings. A port
pairs a door with a setting where it fails. The reference is the smallest door of the same size
that passes the target setting (confirmed with the final grade). A "retime search" also tries
every timing edit of the start door (repeater delays and facings, observer facings, repeater ↔
observer swaps) singly and up to 1,500 random pairs under the target physics. A hit is a known
same-volume port. Then the same single-edit brute force as above, under the target physics.
`max_volume` = max(start volume, reference volume).

**Hidden rule.** A port whose `physics` is not shown to the agent (`physics_told: false`).

Grading ladder used everywhere: a 1-cycle screen (`rules.CYCLES["screen"] = 1`, patched in
process only), then dev (3 cycles), then final (8 cycles with idle offsets). The screen job is
exactly the first cycle of the dev job and every whole-run rule only gets more chances to fail
with more cycles, so a screen failure implies dev and final failures. Only screen passes are
re-graded, and only final passes count as fixes.

## The current set (16 Nov 2026)

30 tasks; the full table with stats is in `SUMMARY.md`.

| kind | 2×2 | 3×2 | 3×3 | 4×4 | total |
|---|---|---|---|---|---|
| repair (k = 2–4) | 5 | 6 | 5 | 3 | 19 |
| port | 0 | 2 | 4 | 2 | 8 |
| hidden_rule | 0 | 1 | 1 | 1 | 3 |

- **All 30 verified** by `verify_tasks.py` with the final grade: every start fails, every reference
  passes, and the hack probes are refused (bigger box, door removed, wrong stated size, and for
  repairs, going over the edit budget).
- **Single-edit brute force.** 24 tasks had their whole census neighbourhood graded (1,400–3,976
  edits each) and none has a single-edit fix. The six 4×4 tasks got a partial search
  (1,816–7,416 of 8,960–10,304 edits); none found.
- **The detector works.** Applying only one of a repair's edits gives a door that brute force
  fixes, in 2 of 1,400 ways (the revert, and an observer placed instead).
- **One port was dropped as too easy.** The Opus changed-physics 112 (`w8-3x3-chg-c-opus`) under
  vanilla is fixed by one repeater delay change. It is kept in `data/controls/` but is not in
  `tasks/`.
- **Every repair perturbation was accepted on the first draw.** When each of the k edits breaks
  the door on its own and the edits are at least two cells apart, no single edit restored any of
  the 19 doors.

What the physics matrix (`data/physics_matrix.json`, 45 doors × 9 settings) shows:
- **2×2 doors cannot be ported.** All three pass every setting tried, so the set has no 2×2 port.
- **3×2 doors break only under observer_pulse=3.** 6 of the 7 fail there. Only `w4-3x2-sonnet-b`
  (volume 54) passes, so no 42-volume port is known. The retime search (all single timing edits
  and all 933–1,500 pairs) found none.
- **Ports with a known same-volume solution.** These are the Fable 70 → changed physics
  (reference: the Opus changed-physics 70), the Opus changed-physics 70 → vanilla (reference:
  the Fable 70), and the Fable changed-physics 72 → vanilla (reference: the Fable 70, smaller).
  Each reference is a different design. No timing-only port of the start door was found in any
  of them.
- **Ports with no same-volume port known.** These are both 3×2 ports, Opus 80 → observer_pulse=1
  (reference 112), both 4×4 ports to changed physics (reference 396 against starts of 240 and
  264), and all three hidden-rule tasks.
- **Combined changes break doors that survive each knob alone.** `w2-4x4-fable-a` passes
  repeater_unit=3 alone and observer_delay=3 alone, but fails with both changed.
- **push_limit=8 breaks no vanilla door,** so it is not used.
