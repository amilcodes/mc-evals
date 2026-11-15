"""One agent run: the tools an agent may call, a call budget, and a server-side log.

The session owns the simulator and the log. The agent only ever sees the text each tool
returns, so the final-test parameters and the log stay on this side.
"""
import hashlib
import json
import threading
import time
from pathlib import Path

from . import rules
from .grade import build_job, grade
from .validate import validate, validate_part

# test: `test` calls. sim: `trace` and `view` calls. lab: game ticks advanced in the lab.
DEFAULT_BUDGET = {"test": 150, "sim": 400, "lab": 50000}
LAB_MAX_STEP = 2000         # most ticks one lab call may advance
LAB_MAX_CHANGES = 20000     # most block changes one lab call reports
LAB_WORLD_TICKS = 4000      # most ticks one lab world may run; then the agent starts a new one
ALWAYS_ALLOWED = ("status", "blocks", "submit")   # tools that still work after the time limit


def _short(state):
    return state.replace("minecraft:", "")


def _digest(sub):
    return hashlib.sha256(json.dumps(sub, sort_keys=True).encode()).hexdigest()[:12]


def _change_lines(changes, grep=None, limit=80):
    lines = []
    for c in changes:
        line = f"t={c[0]} ({c[1]},{c[2]},{c[3]}) {_short(c[4])} -> {_short(c[5])}"
        if grep and grep not in line:
            continue
        lines.append("    " + line)
    extra = len(lines) - limit
    return lines[:limit] + ([f"    ... {extra} more lines (use --limit or --grep)"] if extra > 0 else [])


def _doorway_times(n, doors):
    w, h = rules.dims(n)
    out, last = [], None
    for t, d in enumerate(doors):
        if d != last:
            out.append(f"t{t} " + "/".join(d[y * w:(y + 1) * w] for y in reversed(range(h))))
            last = d
    return "  ".join(out[:30])


class Session:
    def __init__(self, kernel, n, track, log_path, budget=None, time_cap=None, reference=None, variant="scratch", minutes=None,
                 resume=False, exclude=(), physics=None, kit=1):
        """resume: carry on the run recorded in log_path after a tool-server restart. Budgets,
        time limit and variant come from the log; calls, lab ticks, best design, submission and
        time already used are restored. Time while no server was running does not count."""
        n = rules.norm(n)
        self.kit = int(kit or 1)   # 1: the frozen first-benchmark tools; 2 adds `film` and detailed test data
        from .kernel import physics_key
        self.physics = physics_key(physics)
        if getattr(kernel, "physics", {}) != self.physics:
            raise ValueError(f"this run's physics {self.physics or 'vanilla'} differ from the simulator's {getattr(kernel, 'physics', {}) or 'vanilla'}")
        self.k, self.n, self.track = kernel, n, track
        self.time_cap = time_cap or rules.TIME_CAP
        self.reference = reference
        self.budget = {**DEFAULT_BUDGET, **(budget or {})}
        self.used = {"test": 0, "sim": 0, "lab": 0}
        self.lab = None           # {"id", "t", "walls", "entity", "cells", "ops"} for the current lab world
        self.lab_count = 0
        self.minutes = minutes    # wall-clock limit, counted from the first tool call; None = no limit
        self.first_call = None
        # The time limit runs on a clock that stops while the machine sleeps (macOS and Linux
        # monotonic clocks both do), so a laptop going to sleep does not use up a run's time.
        self.now = time.monotonic  # replaced in tests
        self.best = None          # lowest-volume design that passed `test`
        self.submitted = None     # the design the agent nominated last
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.t0 = time.time()
        if resume:
            self._restore(n, track, exclude)
            return
        self._log({"kind": "start", "n": n, "track": track, "variant": variant, "rules": rules.RULES_VERSION,
                   "budget": self.budget, "time_cap": self.time_cap, "minutes": minutes, **({"physics": self.physics} if self.physics else {}), **({"kit": self.kit} if self.kit != 1 else {})})

    def _restore(self, n, track, exclude=()):
        old = [json.loads(line) for line in self.log_path.read_text().splitlines() if line.strip()]
        start = old[0]
        if start["kind"] != "start" or (rules.norm(start["n"]), start["track"], start.get("physics") or {}) != (n, track, self.physics):
            raise ValueError(f"{self.log_path} is not a {rules.label(n)} {track} run with physics {self.physics or 'vanilla'}")
        if start.get("rules") != rules.RULES_VERSION:
            raise ValueError(f"{self.log_path} was made under rules {start.get('rules', '0.2')}, not {rules.RULES_VERSION}")
        self.budget = {**DEFAULT_BUDGET, **start["budget"]}
        self.time_cap, self.minutes = start["time_cap"], start.get("minutes")
        self.kit = start.get("kit", 1)
        tests = [e for e in old if e["kind"] == "test" and e.get("stage") != "validation"]
        self.used = {"test": len(tests),
                     "sim": sum(1 for e in old if e["kind"] in ("trace", "view", "film")),
                     "lab": sum(e.get("ticks", 0) for e in old if e["kind"] == "lab")}
        for e in tests:
            if e["valid"] and (self.best is None or e["volume"] < self.best["volume"]):
                self.best = {"volume": e["volume"], "design": e["design"], "digest": e["digest"]}
        submits = [e for e in old if e["kind"] == "submit"]
        if submits:
            s = submits[-1]
            self.submitted = {"design": s["design"], "digest": s["digest"], "volume": s["tested_volume"]}
        self.lab_count = sum(1 for e in old if e["kind"] == "lab" and e["op"] == "new")
        # Log times carry on from the last entry, so the time with no server running is left out.
        last = old[-1]["t"]
        paused = time.time() - self.log_path.stat().st_mtime
        self.t0 = time.time() - last
        first = next((e for e in old if e["kind"] == "first_call"), None)
        excluded = [list(w) for w in exclude]
        if first is not None:
            if "unix" in first and excluded:
                # Wall time since the first call, less the windows (machine asleep) that must not count.
                now = time.time()
                lost = sum(max(0.0, min(b, now) - max(a, first["unix"])) for a, b in excluded)
                active = now - first["unix"] - lost
            else:
                # Older behaviour: count only up to the last log entry; the gap after it is left out.
                active = last - first["t"]
            self.first_call = self.now() - active
        self._log({"kind": "resume", "seconds_since_last_entry": round(paused, 1), "used": self.used,
                   "best": self.best["volume"] if self.best else None, "excluded": excluded,
                   "minutes_used": round((self.now() - self.first_call) / 60, 2) if self.first_call is not None else None})

    # ---------------------------------------------------------------- plumbing

    def _log(self, entry):
        entry = {"t": round(time.time() - self.t0, 2), "unix": round(time.time(), 2), **entry}
        with self.log_path.open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def _spend(self, kind):
        if self.used[kind] >= self.budget[kind]:
            return f"No {kind} calls left (budget {self.budget[kind]}). Use `pd status`; `pd submit` still works."
        self.used[kind] += 1
        return None

    def call_full(self, tool, args):
        """Dispatch one tool call. Returns {"text": shown to the agent, "data": the same facts as JSON or None}."""
        with self.lock:
            fn = getattr(self, "tool_" + tool, None)
            if fn is None:
                return {"text": f"unknown tool {tool!r}", "data": None}
            if self.first_call is None:
                self.first_call = self.now()
                self._log({"kind": "first_call"})
            if self.minutes is not None and tool not in ALWAYS_ALLOWED and self.now() - self.first_call >= self.minutes * 60:
                return {"text": f"Time is up: {self.minutes} minutes have passed since your first tool call. "
                                "Only status, blocks and submit still work.", "data": None}
            try:
                out = fn(**args)
            except TypeError as e:
                return {"text": f"bad arguments for {tool}: {e}", "data": None}
            text, data = out if isinstance(out, tuple) else (out, None)
            if self.minutes is not None:
                left = max(0, int((self.minutes * 60 - (self.now() - self.first_call)) // 60))
                text += f"\n[time left: {left} of {self.minutes} minutes]"
            return {"text": text, "data": data}

    def call(self, tool, args):
        """Dispatch one tool call. Returns the text shown to the agent."""
        return self.call_full(tool, args)["text"]

    def close(self):
        """Nothing to release: the simulator belongs to the caller. Kept so callers can always close a session."""

    def _parse(self, design):
        if not isinstance(design, dict):
            return None, "The design must be a JSON object: {\"initial_state\": ..., \"blocks\": [...]}"
        errors, blocks = validate(design, self.n)
        if errors:
            lines = [f"REJECTED before simulation ({len(errors)} problem(s)):"]
            for e in errors[:25]:
                lines.append(f"  {e['code']}" + (f" at {e['pos']}" if "pos" in e else "") + f": {e['message']}")
            return None, "\n".join(lines)
        return blocks, None

    # ---------------------------------------------------------------- tools

    def tool_status(self):
        lines = [
            f"Task: {rules.label(self.n)} door, {self.track} track, time cap {self.time_cap} ticks per open or close.",
            f"test calls used {self.used['test']}/{self.budget['test']}; trace/view calls used {self.used['sim']}/{self.budget['sim']}; "
            f"lab ticks used {self.used['lab']}/{self.budget['lab']}.",
            *([f"time used: {int((self.now() - self.first_call) // 60)} of {self.minutes} minutes."] if self.minutes is not None else []),
            f"best valid volume so far: {self.best['volume'] if self.best else 'none'}",
            f"submitted: {('volume ' + str(self.submitted['volume']) if self.submitted.get('volume') else 'a design that did not pass test') if self.submitted else 'nothing yet'}",
        ]
        return "\n".join(lines)

    def tool_blocks(self):
        lines = ["Allowed blocks. Properties may be omitted; the game's defaults apply.", "", "Plain blocks (no properties):"]
        lines.append("  " + ", ".join(sorted(_short(b) for b in rules.PLAIN)))
        lines += ["", "Components:"]
        for b, props in rules.COMPONENTS.items():
            desc = "; ".join(f"{k} = {' | '.join(v) if len(v) <= 7 else v[0] + '..' + v[-1]}" for k, v in props.items())
            lines.append(f"  {_short(b)}" + (f": {desc}" if desc else ""))
        return "\n".join(lines)

    def tool_test(self, design):
        blocks, err = self._parse(design)
        if err:
            self._log({"kind": "test", "digest": _digest(design), "valid": False, "stage": "validation"})
            return err + "\n(This did not use a test call.)", {"valid": False, "rejected": True, "refused": False}
        no = self._spend("test")
        if no:
            return no, {"valid": False, "rejected": False, "refused": True}
        r = grade(self.k, design, self.n, self.track, "dev", time_cap=self.time_cap)
        improved = r["valid"] and (self.best is None or r["volume"] < self.best["volume"])
        if improved:
            self.best = {"volume": r["volume"], "design": design, "digest": _digest(design)}
        self._log({"kind": "test", "digest": _digest(design), "valid": r["valid"], "stage": r["stage"], "volume": r["volume"],
                   "dims": r["dims"], "block_count": r["block_count"], "failures": [f["code"] for f in r["failures"]],
                   "open_ticks": r.get("open_ticks"), "close_ticks": r.get("close_ticks"),
                   "flips_passed": r["flips_passed"], "partial": r["partial"],
                   "best": self.best["volume"] if self.best else None, "design": design})
        lines = []
        if r["valid"]:
            w, h, d = r["dims"]
            lines.append(f"VALID. volume {r['volume']} ({w} x {h} x {d}), blocks {r['block_count']}, "
                         f"open {r['open_ticks']} ticks, close {r['close_ticks']} ticks, at rest by tick {r['reset_ticks']}.")
            lines.append(f"bounding box: {r['bbox']['min']} to {r['bbox']['max']}")
            if improved:
                lines.append("This is your best valid design so far.")
        else:
            lines.append(f"INVALID (reached stage: {r['stage']}).")
            for f in r["failures"]:
                lines.append(f"FAIL {f['code']}: {f['message']}")
                if "timeline" in f:
                    lines.append("  doorway over time (rows top to bottom): " + "  ".join(f"t{t} {d}" for t, d in f["timeline"]))
                if "cells" in f:
                    lines.append("  " + "; ".join(f"{c} is {_short(s)}" for c, s in f["cells"]))
                if f.get("changes"):
                    lines.append("  first block changes in that phase:")
                    lines += _change_lines(f["changes"], limit=30)
            if r["volume"] is not None:
                lines.append(f"(volume would be {r['volume']}, {r['dims'][0]} x {r['dims'][1]} x {r['dims'][2]})")
        for w in r["warnings"]:
            lines.append(f"note (not a failure) {w['code']}: {w['message']}: {w.get('positions')}")
        lines.append(f"[test calls left: {self.budget['test'] - self.used['test']}; best valid volume: {self.best['volume'] if self.best else 'none'}]")
        data = {"valid": r["valid"], "rejected": False, "refused": False, "stage": r["stage"], "volume": r["volume"], "dims": r["dims"],
                "failures": [f["code"] for f in r["failures"]], "open_ticks": r.get("open_ticks"), "close_ticks": r.get("close_ticks"),
                "tests_left": self.budget["test"] - self.used["test"]}
        if self.kit >= 2:
            # Kit 2: the same facts as the report, structured. Failure detail without the raw change lists.
            data["bbox"] = r.get("bbox")
            data["block_count"] = r["block_count"]
            data["timings"] = r.get("timings")
            data["detail"] = [{k: v for k, v in f.items() if k != "changes"} for f in r["failures"]]
        return "\n".join(lines), data

    def _sim(self, blocks, flips, ticks, max_changes=None):
        lever = next(p for p, (bid, _) in blocks.items() if bid == "minecraft:lever")
        job = build_job(self.n, blocks, lever, "dev", self.time_cap)
        steps = job["steps"][:4]
        cap = {"max_changes": max_changes} if max_changes else {}
        if cap:
            steps[2] = {**steps[2], **cap}
        for i in range(flips):
            steps.append({"op": "lever", "label": f"lever.{i}", "pos": list(lever)})
            steps.append({"op": "run", "label": f"move.{i}", "max_ticks": ticks, "quiet": rules.QUIET, **cap})
        steps.append({"op": "snapshot", "label": "end"})
        job["steps"] = steps
        res = self.k.run_job(job)
        return res, {s["label"]: s for s in res["steps"] if "label" in s}

    def tool_trace(self, design, flips=2, ticks=None, grep=None, limit=80):
        """Every block change, tick by tick, after placement and after each lever flip."""
        blocks, err = self._parse(design)
        if err:
            return err
        no = self._spend("sim")
        if no:
            return no
        flips = max(0, min(int(flips), 8))
        ticks = max(1, min(int(ticks or self.time_cap + rules.QUIET), 2000))
        res, steps = self._sim(blocks, flips, ticks)
        self._log({"kind": "trace", "digest": _digest(design), "flips": flips})
        n, out = self.n, []
        s = steps["settle"]
        out.append(f"placement: {'at rest' if s['quiescent'] else 'STILL CHANGING'} after tick {s['last_change_tick']}; "
                   f"doorway {_doorway_times(n, s['door'][-1:])[3:]}  (# door block, . air, m moving, ? other; rows top to bottom)")
        out += _change_lines(s["changes"], grep, limit)
        for i in range(flips):
            lv, mv = steps[f"lever.{i}"], steps[f"move.{i}"]
            if "error" in lv:
                out.append(f"flip {i + 1}: {lv['error']}")
                break
            rest = f"at rest after tick {mv['last_change_tick']}" if mv["quiescent"] else f"STILL CHANGING at tick {mv['ticks']}"
            out.append(f"flip {i + 1} (lever {'on' if lv['powered'] else 'off'}): {rest}; {mv['changes_total']} block changes; doorway: {_doorway_times(n, mv['door'])}")
            # Changes made at the instant of the flip (dust power, lamps) carry t=0.
            out += _change_lines([c for c in lv.get("changes", []) if c[1:4] != lv.get("pos")] + mv["changes"], grep, limit)
        if res["entity_seen"]:
            out.append(f"ENTITY appeared: {res['entity_seen']['type']} at run tick {res['entity_seen']['job_tick']} (invalid)")
        if res["frozen_violation"]:
            v = res["frozen_violation"]
            out.append(f"PROTECTED CELL changed: {v['pos']} became {_short(v['found'])} at run tick {v['job_tick']} (invalid)")
        if res["swept"]:
            out.append(f"swept box so far: {res['swept']['min']} to {res['swept']['max']}")
        out.append(f"[trace/view calls left: {self.budget['sim'] - self.used['sim']}]")
        return "\n".join(out)

    def tool_film(self, design, flips=2, ticks=None):
        """Kit 2. The same simulation as trace, returned as data: the build at rest, then every
        tick of every flip with the doorway and each block change. Uses one trace/view call."""
        if self.kit < 2:
            return "unknown tool 'film'"
        blocks, err = self._parse(design)
        if err:
            return err
        no = self._spend("sim")
        if no:
            return no
        flips = max(1, min(int(flips), 8))
        ticks = max(1, min(int(ticks or self.time_cap + rules.QUIET), 2000))
        res, steps = self._sim(blocks, flips, ticks, max_changes=LAB_MAX_CHANGES)
        self._log({"kind": "film", "digest": _digest(design), "flips": flips})
        n = self.n
        w, h = rules.dims(n)
        rows = lambda d: "/".join(d[y * w:(y + 1) * w] for y in reversed(range(h)))
        ch = lambda c: [c[1], c[2], c[3], _short(c[4]), _short(c[5])]
        s = steps["settle"]
        film = {
            "task": {"width": w, "height": h, "track": self.track},
            "placement": {"at_rest": s["quiescent"], "last_change_tick": s["last_change_tick"],
                          "changes": [[c[0], *ch(c)] for c in s["changes"]]},
            "start": {"doorway": rows(s["door"][-1]),
                      "blocks": [[c[0], c[1], c[2], _short(c[3])] for c in steps["rest.start"]["cells"] if not rules.in_shell(n, c[:3])]},
            "flips": [],
        }
        text = [f"placement: {'at rest' if s['quiescent'] else 'STILL CHANGING'} after tick {s['last_change_tick']}; doorway {film['start']['doorway']}"]
        for i in range(flips):
            lv, mv = steps[f"lever.{i}"], steps[f"move.{i}"]
            if "error" in lv:
                film["flips"].append({"flip": i + 1, "error": lv["error"]})
                text.append(f"flip {i + 1}: {lv['error']}")
                break
            by_tick = {}
            for c in lv.get("changes", []):
                if c[1:4] != lv.get("pos"):
                    by_tick.setdefault(0, []).append(ch(c))
            for c in mv["changes"]:
                by_tick.setdefault(c[0], []).append(ch(c))
            door = mv["door"]
            last = max([mv["last_change_tick"], *by_tick] + [t for t in range(1, len(door)) if door[t] != door[t - 1]])
            last = min(last, len(door) - 1)
            film["flips"].append({
                "flip": i + 1, "lever": "on" if lv["powered"] else "off", "at_rest": mv["quiescent"],
                "last_change_tick": mv["last_change_tick"], "ticks_run": mv["ticks"],
                "changes_total": mv["changes_total"] + len(by_tick.get(0, [])),
                "complete": mv["changes_total"] == len(mv["changes"]),
                "ticks": [{"t": t, "doorway": rows(door[t]), "changes": by_tick.get(t, [])} for t in range(last + 1)],
            })
            rest = f"at rest after tick {mv['last_change_tick']}" if mv["quiescent"] else f"STILL CHANGING at tick {mv['ticks']}"
            text.append(f"flip {i + 1} (lever {'on' if lv['powered'] else 'off'}): {rest}; {film['flips'][-1]['changes_total']} block changes; "
                        f"doorway: {_doorway_times(n, door)}")
        film["entity"] = ({"type": res["entity_seen"]["type"], "run_tick": res["entity_seen"]["job_tick"]} if res["entity_seen"] else None)
        v = res["frozen_violation"]
        film["protected_cell"] = {"pos": v["pos"], "became": _short(v["found"]), "run_tick": v["job_tick"]} if v else None
        film["swept_box"] = res["swept"] or None
        if film["entity"]:
            text.append(f"ENTITY appeared: {film['entity']['type']} at run tick {film['entity']['run_tick']} (invalid)")
        if v:
            text.append(f"PROTECTED CELL changed: {v['pos']} became {_short(v['found'])} at run tick {v['job_tick']} (invalid)")
        text.append(f"[trace/view calls left: {self.budget['sim'] - self.used['sim']}]")
        return "\n".join(text), film

    def _draw(self, cells, title, z, walls):
        """ASCII grids, one per z layer, of a {position: state} map. `walls`: the hallway walls are present."""
        shell = (lambda p: rules.in_shell(self.n, p)) if walls else (lambda p: False)
        mine = [p for p in cells if not shell(p)] or [(0, 0, 0)]
        lo = [min(min(p[i] for p in mine), 0) - 1 for i in range(3)]
        hi = [max(max(p[i] for p in mine), rules.dims(self.n)[i] - 1 if i < 2 else 0) + 1 for i in range(3)]
        if z is not None:
            zs = [int(v) for v in str(z).replace("..", ",").split(",")]
            lo[2], hi[2] = min(zs), max(zs)
        legend, letters = {}, iter("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@$&*+=<>^~")
        out = [f"{title} x runs left to right (west to east), y bottom to top; one grid per z layer.",
               "  . air   _ empty doorway cell   D door block in doorway   # stone" + ("   % hallway wall (harness)" if walls else "")]
        for zz in range(lo[2], hi[2] + 1):
            out.append(f"z = {zz}   (x from {lo[0]} to {hi[0]})")
            for y in range(hi[1], lo[1] - 1, -1):
                row = []
                for x in range(lo[0], hi[0] + 1):
                    p, st = (x, y, zz), cells.get((x, y, zz))
                    if shell(p):
                        ch = "%" if st else "!"
                    elif rules.in_doorway(self.n, p):
                        ch = "_" if not st else "D" if st == rules.DOOR_BLOCK else None
                    elif not st:
                        ch = "."
                    elif st == "minecraft:stone":
                        ch = "#"
                    else:
                        ch = None
                    if ch is None:
                        if st not in legend:
                            legend[st] = next(letters, "?")
                        ch = legend[st]
                    row.append(ch)
                out.append(f"  y={y:>3}  " + "".join(row))
        if legend:
            out.append("legend:")
            out += [f"  {ch} = {_short(st)}" for st, ch in legend.items()]
        return out

    def tool_view(self, design, flips=0, z=None):
        """ASCII slices of the build (one per z layer) after placement and `flips` lever flips."""
        blocks, err = self._parse(design)
        if err:
            return err
        no = self._spend("sim")
        if no:
            return no
        flips = max(0, min(int(flips), 8))
        res, steps = self._sim(blocks, flips, self.time_cap + rules.QUIET)
        self._log({"kind": "view", "digest": _digest(design), "flips": flips})
        cells = {tuple(c[:3]): c[3] for c in steps["end"]["cells"]}
        out = self._draw(cells, f"State after placement and {flips} lever flip(s).", z, walls=True)
        out.append(f"[trace/view calls left: {self.budget['sim'] - self.used['sim']}]")
        return "\n".join(out)

    # ---------------------------------------------------------------- the lab
    #
    # A free-form world for trying out parts. Every lab call rebuilds the lab world from scratch
    # in the shared simulator: it clears the area, places the lab's blocks, replays every flip and
    # every tick run so far, then does the new operation. The simulator is deterministic, so the
    # world is exactly as the last call left it, and tests or other runs using the same simulator
    # in between cannot disturb it. Nothing ticks between calls.

    def _lab_job(self, steps, cells=None):
        """Runs `steps` on the current lab world (or on a fresh one holding `cells`). Returns the
        kernel result with only the results of `steps`."""
        lo, hi = rules.region(self.n)
        history = [] if cells is not None else self.lab["ops"]
        cells = cells if cells is not None else self.lab["cells"]
        w, h = rules.dims(self.n)
        job = {"origin": list(rules.ORIGIN), "region": {"min": list(lo), "max": list(hi)}, "n": w, "w": w, "h": h,
               "door_block": rules.DOOR_BLOCK, "ignore": [], "frozen": [],
               "steps": [{"op": "clear"}, {"op": "place", "blocks": cells, "observers_fire_on_place": False}, *history, *steps]}
        res = self.k.run_job(job)
        res["steps"] = res["steps"][len(job["steps"]) - len(steps):]
        return res

    def _lab_check(self, lab):
        if self.lab is None:
            if self.lab_count:
                return "The lab world is gone: the tool server was restarted. Start a new one (lab new)."
            return "There is no lab world yet. Start one first (lab new)."
        if lab is not None and lab != self.lab["id"]:
            return f"Lab {lab} no longer exists: a newer lab world (lab {self.lab['id']}) replaced it."
        return None

    def _lab_cells(self, with_walls=False):
        """Current non-air cells of the lab; the hallway-wall cells are left out unless asked for."""
        res = self._lab_job([{"op": "snapshot"}])
        skip = self.lab["walls"] and not with_walls
        return {tuple(c[:3]): c[3] for c in res["steps"][0]["cells"] if not (skip and rules.in_shell(self.n, c[:3]))}

    def _lab_doorway(self, cells):
        def ch(state):
            if state is None:
                return "."
            return "#" if state == rules.DOOR_BLOCK else "m" if rules.parse_state(state)[0] == "minecraft:moving_piston" else "?"
        w, h = rules.dims(self.n)
        return "/".join("".join(ch(cells.get((x, y, 0))) for x in range(w)) for y in reversed(range(h)))

    def tool_lab_new(self, blocks, walls=False):
        """Empty the lab world and place these blocks in it. The lab clock restarts at 0."""
        items = blocks.get("blocks") if isinstance(blocks, dict) else blocks
        walls = bool(walls)
        errors, placed = validate_part(items, self.n, walls)
        if errors:
            lines = [f"REJECTED ({len(errors)} problem(s)); the lab was left as it was:"]
            for e in errors[:25]:
                lines.append(f"  {e['code']}" + (f" at {e['pos']}" if "pos" in e else "") + f": {e['message']}")
            return "\n".join(lines), None
        cells = [[*c, rules.WALL_BLOCK] for c in rules.shell(self.n)] if walls else []
        cells += [[*pos, rules.state_string(bid, props)] for pos, (bid, props) in sorted(placed.items())]
        res = self._lab_job([{"op": "snapshot"}], cells=cells)
        now = {tuple(c[:3]): c[3] for c in res["steps"][0]["cells"]}
        lost = [list(pos) for pos, (bid, _) in sorted(placed.items()) if rules.parse_state(now.get(pos, "minecraft:air"))[0] != bid]
        self.lab_count += 1
        self.lab = {"id": self.lab_count, "t": 0, "walls": walls, "entity": False, "cells": cells, "ops": []}
        self._log({"kind": "lab", "op": "new", "lab": self.lab["id"], "walls": walls, "blocks": items})
        lines = [f"Lab {self.lab['id']} started: {len(placed)} block(s) placed, hallway walls {'present' if walls else 'absent'}, clock t=0."]
        if lost:
            lines.append(f"note: these blocks could not exist where they were put and are gone: {lost[:20]}")
        return "\n".join(lines), {"lab": self.lab["id"], "t": 0, "placed": len(placed), "lost": lost}

    def tool_lab_flip(self, pos, lab=None):
        """Flip the lever at pos. No tick passes."""
        no = self._lab_check(lab)
        if no:
            return no, None
        if not (isinstance(pos, (list, tuple)) and len(pos) == 3 and all(type(c) is int for c in pos)):
            return "pos must be three whole numbers: [x, y, z]", None
        pos, t = list(pos), self.lab["t"]
        r = self._lab_job([{"op": "lever", "pos": pos}])["steps"][0]
        if "error" in r:
            return f"lab t={t}: {r['error']}. Nothing was changed.", None
        self.lab["ops"].append({"op": "lever", "pos": pos})
        changes = [[t, c[1], c[2], c[3], _short(c[4]), _short(c[5])] for c in r["changes"] if c[1:4] != pos]
        self._log({"kind": "lab", "op": "flip", "lab": self.lab["id"], "t": t, "pos": pos})
        lines = [f"lab t={t}: lever at ({pos[0]},{pos[1]},{pos[2]}) switched {'on' if r['powered'] else 'off'}; "
                 f"{len(changes)} other block(s) changed at that instant"]
        lines += _change_lines(changes, None, 80)
        return "\n".join(lines), {"lab": self.lab["id"], "t": t, "powered": r["powered"], "changes": changes}

    def _lab_run(self, op, step, grep, limit):
        t0 = self.lab["t"]
        res = self._lab_job([{"op": "run", "max_changes": LAB_MAX_CHANGES, **step}])
        r = res["steps"][0]
        self.lab["ops"].append({"op": "run", "max_ticks": r["ticks"], "min_ticks": r["ticks"], "max_changes": 0})
        self.lab["t"] += r["ticks"]
        self.used["lab"] += r["ticks"]
        changes = [[t0 + c[0], c[1], c[2], c[3], _short(c[4]), _short(c[5])] for c in r["changes"]]
        entity = None
        if res["entity_seen"] and not self.lab["entity"]:
            self.lab["entity"] = True
            entity = {"t": res["entity_seen"]["job_tick"], "type": res["entity_seen"]["type"]}
        self._log({"kind": "lab", "op": op, "lab": self.lab["id"], "t": self.lab["t"], "ticks": r["ticks"]})
        left = self.budget["lab"] - self.used["lab"]
        data = {"lab": self.lab["id"], "t": self.lab["t"], "ticks": r["ticks"], "changes": changes,
                "changes_total": r["changes_total"], "entity": entity, "ticks_left": left}
        tail = _change_lines(changes, grep, max(0, int(limit)))
        if r["changes_total"] > len(changes):
            tail.append(f"    (only the first {len(changes)} of {r['changes_total']} changes are listed; advance fewer ticks per call to see all)")
        if entity:
            tail.append(f"ENTITY appeared at t={entity['t']}: {entity['type']} (an item drop or falling block; in a door this is a failure)")
        tail.append(f"[lab ticks left: {left}]")
        return r, t0, data, tail

    def tool_lab_step(self, ticks=1, grep=None, limit=80, lab=None):
        """Advance the lab by exactly `ticks` game ticks."""
        no = self._lab_check(lab)
        if no:
            return no, None
        if type(ticks) is not int or not 1 <= ticks <= LAB_MAX_STEP:
            return f"ticks must be a whole number from 1 to {LAB_MAX_STEP}", None
        left = self.budget["lab"] - self.used["lab"]
        if ticks > left:
            return f"Only {left} lab tick(s) left (budget {self.budget['lab']}), fewer than the {ticks} asked for. Nothing was run.", None
        room = LAB_WORLD_TICKS - self.lab["t"]
        if ticks > room:
            return (f"This lab world is at t={self.lab['t']}, and one lab world can run at most {LAB_WORLD_TICKS} ticks. "
                    f"Step at most {room}, or start a new lab. Nothing was run."), None
        r, t0, data, tail = self._lab_run("step", {"max_ticks": ticks, "min_ticks": ticks}, grep, limit)
        head = f"lab t={t0} -> t={self.lab['t']}: {r['changes_total']} block change(s)"
        return "\n".join([head] + tail), data

    def tool_lab_rest(self, max_ticks=200, grep=None, limit=80, lab=None):
        """Advance the lab until no block has changed for QUIET ticks in a row, or for max_ticks."""
        no = self._lab_check(lab)
        if no:
            return no, None
        if type(max_ticks) is not int or not 1 <= max_ticks <= LAB_MAX_STEP:
            return f"max_ticks must be a whole number from 1 to {LAB_MAX_STEP}", None
        left = self.budget["lab"] - self.used["lab"]
        if left <= 0:
            return f"No lab ticks left (budget {self.budget['lab']}). Nothing was run.", None
        room = LAB_WORLD_TICKS - self.lab["t"]
        if room <= 0:
            return (f"This lab world has run the most ticks one lab world can run ({LAB_WORLD_TICKS}). "
                    "Start a new lab. Nothing was run."), None
        capped = left < max_ticks and left <= room
        world_capped = room < max_ticks and room < left
        r, t0, data, tail = self._lab_run("rest", {"max_ticks": min(max_ticks, left, room), "quiet": rules.QUIET}, grep, limit)
        last = t0 + r["last_change_tick"] if r["last_change_tick"] else None
        data.update({"at_rest": r["quiescent"], "last_change": last})
        if r["quiescent"]:
            what = f"at rest; {'last block change at t=' + str(last) if last is not None else 'no block changed'}"
        else:
            what = f"STILL CHANGING after {r['ticks']} ticks" + (" (stopped by the lab tick budget)" if capped else
                                                                 f" (stopped at the {LAB_WORLD_TICKS}-tick limit for one lab world)" if world_capped else "")
        head = f"lab t={t0} -> t={self.lab['t']}: {what}; {r['changes_total']} block change(s)"
        return "\n".join([head] + tail), data

    def tool_lab_look(self, cells=None, grep=None, lab=None):
        """The current state of the lab's blocks. No tick passes."""
        no = self._lab_check(lab)
        if no:
            return no, None
        everything = self._lab_cells(with_walls=True)
        skip = self.lab["walls"]
        now = {p: st for p, st in everything.items() if not (skip and rules.in_shell(self.n, p))}
        if cells is None:
            listing = sorted(now.items())           # every block; the hallway walls are left out
        else:
            if not (isinstance(cells, list) and all(isinstance(c, (list, tuple)) and len(c) == 3 and all(type(v) is int for v in c) for c in cells)):
                return "cells must be a list of [x, y, z] positions", None
            listing = [(tuple(c), everything.get(tuple(c), "minecraft:air")) for c in cells]   # a named wall cell reads as what it is
        door = self._lab_doorway(now)
        blocks = [[*pos, _short(state)] for pos, state in listing]
        lines = [f"lab t={self.lab['t']}: {len(now)} block(s) in the lab; doorway {door}  (rows top to bottom; # stone, . air, m moving, ? other)"]
        for x, y, z, state in blocks:
            line = f"  ({x},{y},{z}) {state}"
            if not grep or grep in line:
                lines.append(line)
        return "\n".join(lines), {"lab": self.lab["id"], "t": self.lab["t"], "blocks": blocks, "doorway": door}

    def tool_lab_view(self, z=None, lab=None):
        """ASCII slices of the lab as it is now. No tick passes."""
        no = self._lab_check(lab)
        if no:
            return no, None
        cells = self._lab_cells(with_walls=True)
        return "\n".join(self._draw(cells, f"Lab at t={self.lab['t']}.", z, walls=self.lab["walls"])), None

    def tool_submit(self, design):
        """Nominate the design to be scored. The last submission counts."""
        blocks, err = self._parse(design)
        if err:
            return err + "\nNot submitted."
        digest = _digest(design)
        volume = self.best["volume"] if self.best and self.best["digest"] == digest else None
        if volume is None:
            for line in self.log_path.read_text().splitlines():
                e = json.loads(line)
                if e.get("kind") == "test" and e.get("digest") == digest and e.get("valid"):
                    volume = e["volume"]
        self.submitted = {"design": design, "digest": digest, "volume": volume}
        self._log({"kind": "submit", "digest": digest, "tested_volume": volume, "design": design})
        if volume is None:
            return ("Submitted, but this exact design has not passed `pd test`. It will be scored as submitted; "
                    "if it fails the final test the score is 0.")
        note = "" if not self.best or volume <= self.best["volume"] else f" Note: you have a smaller valid design (volume {self.best['volume']})."
        return f"Submitted the design with tested volume {volume}. It will get one final test with more cycles and varied timing.{note}"
