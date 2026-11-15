"""Tool server for one agent run, plus final scoring from its log.

serve(): a localhost HTTP endpoint. POST / with {"tool": name, "args": {...}} returns
{"text": what the agent reads, "data": the same facts as JSON, or null}.
score(): picks the design to score from the log and gives it the final test in a fresh simulator.
"""
import json
import signal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import references, rules
from .grade import grade, translation_pass_rate
from .kernel import Kernel
from .session import Session


def _handler(session):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            try:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                reply = session.call_full(str(body.get("tool")), body.get("args") or {})
            except Exception as e:  # never show the agent a stack trace from this side
                session._log({"kind": "error", "error": repr(e)})
                reply = {"text": f"tool server error: {type(e).__name__}: {e}", "data": None}
            data = json.dumps(reply).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *a):
            pass

    return Handler


def serve(n, track, log_path, port, budget=None, time_cap=None, host="127.0.0.1", variant="scratch", minutes=None, resume=False, physics=None, kit=1):
    kernel = Kernel(physics=physics)
    session = Session(kernel, n, track, log_path, budget=budget, time_cap=time_cap, variant=variant, minutes=minutes, resume=resume,
                      physics=physics, kit=kit)
    Handler = _handler(session)

    def stop(*_):  # a plain `kill` should also shut the simulator down and remove its temp folder
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"pdgrader serving {rules.label(n)} {track} on http://{host}:{port} (log: {log_path})", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        session.close()
        kernel.close()


def serve_many(specs, host="127.0.0.1", resume=False, exclude=()):
    """Several agent runs in one process, all sharing one simulator, each on its own port.

    specs: [{"port", "n", "track", "log", "variant"?, "minutes"?, "budget"?, "physics"?}]. Simulator
    jobs take turns; every run's results are the same as with a simulator of its own, because
    every job (lab calls included) starts from a cleared area. Runs with the same physics share
    one simulator; each distinct physics setting gets its own.
    """
    import threading
    from .kernel import physics_key
    kernels = {}
    servers = []
    for sp in specs:
        key = json.dumps(physics_key(sp.get("physics")))
        if key not in kernels:
            kernels[key] = Kernel(physics=sp.get("physics"))
        session = Session(kernels[key], sp["n"], sp["track"], sp["log"], budget=sp.get("budget"), variant=sp.get("variant", "scratch"),
                          minutes=sp.get("minutes"), resume=resume, exclude=exclude, physics=sp.get("physics"), kit=sp.get("kit_version", 1))
        httpd = ThreadingHTTPServer((host, sp["port"]), _handler(session))
        servers.append(httpd)
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        print(f"pdgrader serving {rules.label(sp['n'])} {sp['track']} on http://{host}:{sp['port']} (log: {sp['log']})", flush=True)

    def stop(*_):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        for httpd in servers:
            httpd.shutdown()
        for kernel in kernels.values():
            kernel.close()


def read_log(log_path):
    return [json.loads(line) for line in Path(log_path).read_text().splitlines() if line.strip()]


def score(log_path, reference=None, translations=True):
    """Final verdict for a run. Candidate: the last `submit`, else the smallest design that passed `test`.

    With no `reference` given, the task's entry in references.py is used if there is one.
    """
    log = read_log(log_path)
    start = next(e for e in log if e["kind"] == "start")
    n, track = rules.norm(start["n"]), start["track"]
    legacy = "rules" not in start  # a run made before rulebook 0.3 keeps the placement rule it was built under
    physics = start.get("physics") or {}
    from_table = reference is None
    if from_table:
        reference = references.reference(n, track, physics)
    tests = [e for e in log if e["kind"] == "test"]
    valid = [e for e in tests if e.get("valid")]
    submits = [e for e in log if e["kind"] == "submit"]
    first = next((e["t"] for e in log if e["kind"] == "first_call"), None)
    out = {
        "n": n, "track": track, "physics": physics, "kit": start.get("kit", 1), "variant": start.get("variant", "scratch"), "rules": start.get("rules", "0.2"), "seconds": log[-1]["t"],
        "minutes_limit": start.get("minutes"),
        # From the agent's first tool call to its last, and to its first valid test.
        "seconds_active": round(log[-1]["t"] - first, 2) if first is not None else None,
        "seconds_to_first_valid": next((round(e["t"] - (first or 0), 2) for e in log if e["kind"] == "test" and e.get("valid")), None),
        "reference": reference, "reference_verified": references.verified(n, track, physics) if from_table and reference else None,
        "test_calls": sum(1 for e in tests if e.get("stage") != "validation"),
        "rejected_before_simulation": sum(1 for e in tests if e.get("stage") == "validation"),
        "sim_calls": sum(1 for e in log if e["kind"] in ("trace", "view", "film")),
        "lab_worlds": sum(1 for e in log if e["kind"] == "lab" and e["op"] == "new"),
        "server_restarts": sum(1 for e in log if e["kind"] == "resume"),
        "lab_ticks": sum(e.get("ticks", 0) for e in log if e["kind"] == "lab"),
        "valid_tests": len(valid),
        "first_valid_at_test": next((i + 1 for i, e in enumerate(tests) if e.get("valid")), None),
        "best_dev_volume": min((e["volume"] for e in valid), default=None),
        # Diagnostic for runs with no valid door: the furthest any tested design got (1.0 = passed).
        "best_partial": max((e.get("partial", 0.0) for e in tests), default=0.0),
        "progress": [[i + 1, e["best"]] for i, e in enumerate(tests) if e.get("valid") and e["volume"] == e["best"]],
    }
    if submits:
        candidate, out["candidate_source"] = submits[-1]["design"], "last submit"
    elif valid:
        candidate, out["candidate_source"] = min(valid, key=lambda e: e["volume"])["design"], "best tested (no submit)"
    else:
        out.update({"candidate_source": None, "final": None, "valid": False, "volume": None, "score": 0.0 if reference else None})
        return out
    with Kernel(physics=physics) as k:  # a fresh simulator with the run's physics, as the rulebook requires for the final test
        final = grade(k, candidate, n, track, "final", time_cap=start.get("time_cap"), reference=reference, legacy_placement=legacy)
        if final["valid"] and translations:
            out["translations"] = translation_pass_rate(k, candidate, n, track, legacy_placement=legacy)
    out["valid"], out["volume"], out["dims"] = final["valid"], final["volume"] if final["valid"] else None, final["dims"]
    out["block_count"] = final["block_count"]
    out["final_partial"] = final["partial"]
    out["open_ticks"], out["close_ticks"] = final.get("open_ticks"), final.get("close_ticks")
    out["final_failures"] = [{"code": f["code"], "message": f["message"]} for f in final["failures"]]
    out["score"] = final.get("score")
    out["candidate"] = candidate
    return out
