"""Task assembly helpers shared by make_tasks.py and check.py."""
import json
from pathlib import Path

import lib
from circuits import CIRCUITS

HERE = Path(__file__).resolve().parent
TASKS = HERE / "tasks"
REFS = HERE / "refs"


def bbox_of(builds, harness, pad_xz=1, pad_up=1):
    pts = [tuple(b["pos"]) for bl in builds for b in bl] + [p for p, _, _ in lib.harness_blocks(harness)]
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    return {"min": [lo[0] - pad_xz, min(lo[1], 0), lo[2] - pad_xz], "max": [hi[0] + pad_xz, hi[1] + pad_up, hi[2] + pad_xz]}


def spec_from(circuit, outputs, tol=0, latency=(0, 0)):
    ev, end = circuit["schedule"]
    return {"inputs": ev, "end": end, "tol": tol, "latency": list(latency),
            "outputs": {k: {"initial": bool(v[0]), "edges": [[t, bool(x)] for t, x in v[1]]} for k, v in outputs.items()}}


def skeleton(circuit, builds, spec, physics=None, slack=4, max_blocks=None):
    return {"harness": circuit["harness"],
            "limits": {"bbox": bbox_of(builds, circuit["harness"]),
                       "max_blocks": max_blocks or max(len(b) for b in builds) + slack},
            "spec": spec, "physics": physics or {}}


def load_task(path):
    return json.loads(Path(path).read_text())
