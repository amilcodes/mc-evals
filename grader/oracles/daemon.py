#!/usr/bin/env python3
"""Keeps one simulator alive and serves view/trace/test/final/probe over localhost HTTP.
Only used while developing the oracle; not part of the grader."""
import json, sys, tempfile, traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

G = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(G))
from pdgrader import rules
from pdgrader.kernel import Kernel
from pdgrader.session import Session
from pdgrader.grade import grade, translation_pass_rate, build_job
from pdgrader.validate import validate

PORT = 8877
k = Kernel()
s = Session(k, 3, "seamless", tempfile.mktemp(suffix=".jsonl"), budget={"test": 10**9, "sim": 10**9})


def short(x):
    return x.replace("minecraft:", "")


def probe(design, flips=1, ticks=60, cells=None, settle=20, all_changes=False):
    """Per-tick state of chosen cells (including dust power), via one snapshot per tick."""
    errors, blocks = validate(design, 3)
    if errors:
        return "REJECTED: " + json.dumps(errors[:10])
    lever = next(p for p, (bid, _) in blocks.items() if bid == "minecraft:lever")
    job = build_job(3, blocks, lever, "dev", 200)
    steps = job["steps"][:2]
    labels = []
    def tick_steps(tag, n):
        for t in range(1, n + 1):
            steps.append({"op": "run", "label": f"r.{tag}.{t}", "max_ticks": 1, "min_ticks": 1})
            steps.append({"op": "snapshot", "label": f"s.{tag}.{t}"})
            labels.append((tag, t))
    steps.append({"op": "snapshot", "label": "s.place.0"})
    labels.append(("place", 0))
    tick_steps("place", settle)
    for i in range(flips):
        steps.append({"op": "lever", "label": f"lever.{i}", "pos": list(lever)})
        steps.append({"op": "snapshot", "label": f"s.flip{i+1}.0"})
        labels.append((f"flip{i+1}", 0))
        tick_steps(f"flip{i+1}", ticks)
    job["steps"] = steps
    res = k.run_job(job)
    by = {st["label"]: st for st in res["steps"] if "label" in st}
    shell = set(rules.shell(3))
    want = {tuple(c) for c in cells} if cells else None
    prev, out = None, []
    for tag, t in labels:
        cur = {tuple(c[:3]): c[3] for c in by[f"s.{tag}.{t}"]["cells"] if tuple(c[:3]) not in shell}
        if prev is None:
            prev = cur
            continue
        keys = sorted(set(cur) | set(prev))
        for p in keys:
            if want is not None and p not in want:
                continue
            a, b = prev.get(p, "air"), cur.get(p, "air")
            if a != b:
                out.append(f"{tag} t={t} {p} {short(a)} -> {short(b)}")
        prev = cur
    if res["entity_seen"]:
        out.append(f"ENTITY {res['entity_seen']}")
    if res["frozen_violation"]:
        out.append(f"FROZEN {res['frozen_violation']}")
    return "\n".join(out)


def final(design):
    lines = []
    for track in ("seamless", "open"):
        r = grade(k, design, 3, track, "final")
        lines.append(f"final {track}: valid={r['valid']} volume={r['volume']} dims={r['dims']} blocks={r['block_count']} "
                     f"open={r.get('open_ticks')} close={r.get('close_ticks')} reset={r.get('reset_ticks')} stage={r['stage']}")
        for f in r["failures"]:
            lines.append(f"  FAIL {f['code']}: {f['message']}")
            if "timeline" in f:
                lines.append("   timeline: " + ", ".join(f"{t}:{d}" for t, d in f["timeline"]))
            if "cells" in f:
                lines.append("   cells: " + str(f["cells"]))
        for w in r["warnings"]:
            lines.append(f"  warn {w['code']}: {w.get('positions')}")
        if r["valid"]:
            t = translation_pass_rate(k, design, 3, track)
            lines.append(f"  translations {track}: {t['passed']}/{t['of']} failed={t['failed']}")
    return "\n".join(lines)


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            tool, args = body["tool"], body.get("args", {})
            if tool == "probe":
                text = probe(**args)
            elif tool == "final":
                text = final(**args)
            else:
                text = s.call(tool, args)
        except Exception:
            text = "daemon error:\n" + traceback.format_exc()
        data = json.dumps({"text": text}).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


print("ready", flush=True)
try:
    HTTPServer(("127.0.0.1", PORT), H).serve_forever()
finally:
    k.close()
