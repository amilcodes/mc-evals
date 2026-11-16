"""Records kit-2 films of chosen doors so render.py can draw them.

    python3 make_films.py   ->  films/<name>.json
"""
import json
import sys
import tempfile
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "grader"))
import pdgrader.kernel as K  # noqa: E402
from pdgrader import rules  # noqa: E402
from pdgrader.session import Session  # noqa: E402

SCRATCH = Path("/private/tmp/claude-501/films_k")
SCRATCH.mkdir(parents=True, exist_ok=True)
K.tempfile = types.SimpleNamespace(mkdtemp=lambda prefix="", dir=None: tempfile.mkdtemp(prefix=prefix, dir=str(SCRATCH)))

BENCH = ROOT / "runs/bench"
DOORS = {
    "fable70_fast": (3, BENCH / "search_pilot/fable70_observer.json"),
    "opus240_4x4": (4, BENCH / "w4/w4-4x4-opus-e/result.json"),
    "haiku30_2x2": (2, BENCH / "w2/w2-2x2-haiku-a/result.json"),
}


def load(p):
    d = json.loads(p.read_text())
    return d.get("candidate", d)


out = HERE / "films"
out.mkdir(exist_ok=True)
with K.Kernel(heap="800M") as k:
    for name, (n, path) in DOORS.items():
        design = load(path)
        s = Session(k, n, "seamless", str(SCRATCH / f"{name}.log.jsonl"), kit=2)
        res = s.tool_film(design, flips=2)
        if not isinstance(res, tuple):
            raise SystemExit(f"{name}: {res}")
        film = res[1]
        lo, hi = film["swept_box"]["min"], film["swept_box"]["max"]
        film["walls"] = [list(c) for c in rules.shell(n) if lo[2] - 2 <= c[2] <= hi[2] + 2]
        film["lever"] = next(b["pos"] for b in design["blocks"] if b["id"].endswith("lever"))
        (out / f"{name}.json").write_text(json.dumps(film))
        print(name, "ok", film["flips"][0].get("last_change_tick"), flush=True)
