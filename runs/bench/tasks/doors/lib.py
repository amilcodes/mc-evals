"""Shared helpers for the door repair / port task family.

Everything here reads the project; nothing writes outside runs/bench/tasks/doors and the
kernel scratch folder below. One kernel at a time, heap 1G.
"""
import contextlib
import copy
import json
import shutil
import subprocess
import sys
import tempfile as _tf
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BENCH = ROOT / "runs/bench"
TASKS = HERE / "tasks"
SCRATCH = Path("/private/tmp/claude-501/tasks_doors_k")

sys.path.insert(0, str(ROOT / "grader"))

from pdgrader import rules  # noqa: E402
from pdgrader.grade import grade  # noqa: E402
from pdgrader.kernel import physics_key  # noqa: E402
import importlib.util as _ilu  # noqa: E402

# census.py from the single-edit census (apply / norm / PALETTE), loaded by path so that nothing
# else in search_pilot/ can shadow this folder's modules.
_spec = _ilu.spec_from_file_location("census", BENCH / "search_pilot/census.py")
census = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(census)

# A 1-cycle screen. Its steps are exactly the first cycle of the dev job, and every whole-run
# rule only gets more chances to fail with more cycles, so: screen fails => dev fails => final fails.
rules.CYCLES.setdefault("screen", 1)

VANILLA = {}
CHG = {"repeater_unit": 3, "observer_delay": 3}   # the benchmark's "changed physics" track


def phys_tag(p):
    p = {k: v for k, v in sorted((p or {}).items()) if v != {"repeater_unit": 2, "push_limit": 12, "observer_delay": 2, "observer_pulse": 2}[k]}
    return "vanilla" if not p else ",".join(f"{k}={v}" for k, v in p.items())


def free_mb():
    out = subprocess.run(["df", "-k", "/private/tmp"], capture_output=True, text=True).stdout.splitlines()[-1].split()
    return int(out[3]) // 1024


def wait_for_disk(need_mb=300, tries=10):
    for i in range(tries + 1):
        mb = free_mb()
        if mb >= need_mb:
            return mb
        if i == tries:
            raise SystemExit(f"disk: only {mb} MB free on /private/tmp after {tries} minutes; stopping")
        print(f"disk: {mb} MB free, waiting a minute", flush=True)
        time.sleep(60)


@contextlib.contextmanager
def kernel(physics=None):
    import pdgrader.kernel as K
    wait_for_disk()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    K.tempfile = types.SimpleNamespace(mkdtemp=lambda prefix="", dir=None: _tf.mkdtemp(prefix=prefix, dir=str(SCRATCH)))
    k = K.Kernel(heap="1G", physics=physics or None)
    try:
        yield k
    finally:
        k.close()


def cleanup():
    shutil.rmtree(SCRATCH, ignore_errors=True)


# ---------------------------------------------------------------- doors

def doors():
    """Every verified door: list of dicts with run, n, physics, volume, candidate."""
    out = []
    for r in json.load(open(BENCH / "dashboard/runs.json")):
        if r["status"] != "door":
            continue
        res = json.load(open(BENCH / r["wave"] / r["run"] / "result.json"))
        n = res["n"]
        n = rules.norm(n)
        out.append({"run": r["run"], "model": r.get("model"), "n": n if isinstance(n, int) else list(n),
                    "physics": res.get("physics") or {}, "volume": res["volume"], "open_ticks": res.get("open_ticks"),
                    "close_ticks": res.get("close_ticks"), "candidate": res["candidate"]})
    return out


def door(run):
    return next(d for d in doors() if d["run"] == run)


def size_label(n):
    return rules.label(n)


# ---------------------------------------------------------------- designs and edits

def canon(b):
    """(id, props) with derived state (wire shape/power, powered, lit, extended pairs) normalised away."""
    bid, p = census.norm(b)
    return bid, p


def cells(design):
    return {tuple(b["pos"]): canon(b) for b in design["blocks"]}


def edit_distance(a, b):
    """Number of positions whose (normalised) block differs, plus 1 if initial_state differs."""
    ca, cb = cells(a), cells(b)
    d = sum(1 for p in set(ca) | set(cb) if ca.get(p, ("air", {})) != cb.get(p, ("air", {})))
    return d + (a.get("initial_state") != b.get("initial_state"))


def diff(a, b):
    ca, cb = cells(a), cells(b)
    return [{"pos": list(p), "from": list(ca.get(p, ("air", {}))), "to": list(cb.get(p, ("air", {})))}
            for p in sorted(set(ca) | set(cb)) if ca.get(p, ("air", {})) != cb.get(p, ("air", {}))]


def apply_edits(design, edits):
    s = copy.deepcopy(design)
    for e in edits:
        s = census.apply(s, e)
    s["blocks"].sort(key=lambda b: (b["pos"][2], b["pos"][1], b["pos"][0]))
    return s


def brief(r):
    out = {k: r.get(k) for k in ("valid", "volume", "open_ticks", "close_ticks", "flips_passed", "partial", "block_count")}
    out["fail"] = r["failures"][0]["code"] if r["failures"] else None
    return out


def grade_ladder(k, design, n, final=True):
    """Screen, then dev, then final; stops at the first failure. Returns (passed_stage, brief)."""
    r = grade(k, design, n, "seamless", "screen")
    if not r["valid"]:
        return "screen", brief(r)
    r = grade(k, design, n, "seamless", "dev")
    if not r["valid"]:
        return "dev", brief(r)
    if not final:
        return "dev_ok", brief(r)
    r = grade(k, design, n, "seamless", "final")
    return ("final_ok" if r["valid"] else "final"), brief(r)


def neighbours(design, n):
    """The census neighbourhood (census.neighbours), generalised to rectangular doors: every cell of
    the design's bounding box (doorway included in the box) except the doorway, hallway, hallway
    walls and the lever, set to each of the census's 57 block states other than its current one."""
    w, h = rules.dims(n)
    cs = {tuple(b["pos"]): b for b in design["blocks"]}
    lever = next(tuple(b["pos"]) for b in design["blocks"] if b["id"].endswith("lever"))
    body = [p for p in cs if p != lever]
    lo = [min([p[i] for p in body] + [0]) for i in range(3)]
    hi = [max([p[i] for p in body] + [(w - 1, h - 1, 0)[i]]) for i in range(3)]
    out = []
    for x in range(lo[0], hi[0] + 1):
        for y in range(lo[1], hi[1] + 1):
            for z in range(lo[2], hi[2] + 1):
                pos = (x, y, z)
                if pos == lever or rules.in_doorway(n, pos) or rules.in_hallway(n, pos) or rules.in_shell(n, pos):
                    continue
                cur = canon(cs[pos]) if pos in cs else ("air", {})
                for bid, props in census.PALETTE:
                    if (bid, props) != cur:
                        out.append({"pos": list(pos), "from": [cur[0], cur[1]], "to": [bid, props]})
    return out


def single_edit_fixes(k, design, n, edits=None, stop_at_first=False, log_every=500):
    """Grades every single edit of `design` from the census neighbourhood (or `edits`).
    Returns (fixes, graded). A fix passes the final grade."""
    edits = neighbours(design, n) if edits is None else edits
    fixes, t0 = [], time.monotonic()
    for i, e in enumerate(edits):
        s = census.apply(design, e)
        r = grade(k, s, n, "seamless", "screen")
        if r["valid"]:
            stage, b = grade_ladder(k, s, n)
            if stage == "final_ok":
                fixes.append({**e, "final": b})
                if stop_at_first:
                    return fixes, i + 1
        if log_every and (i + 1) % log_every == 0:
            print(f"    {i + 1}/{len(edits)} graded, {len(fixes)} fixes, {time.monotonic() - t0:.0f}s", flush=True)
    return fixes, len(edits)


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=1) + "\n")
