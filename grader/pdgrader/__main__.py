"""Command line: python -m pdgrader setup | grade."""
import argparse
import json
import sys

from . import kernel as kernel_mod
from . import rules
from .grade import grade, translation_pass_rate


def _size(text):
    """--n: a square size such as 3, or a rectangle such as 3x2 (width x height)."""
    try:
        n = rules.norm(text)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"bad door size {text!r}")
    if not rules.valid_size(n):
        raise argparse.ArgumentTypeError(f"door size must be one of {rules.SIZES} or WxH with sides 1..{rules.MAX_SIDE}")
    return n


def _physics(text):
    """--physics: comma-separated key=value, e.g. repeater_unit=3,push_limit=8."""
    from .kernel import PHYSICS_DEFAULTS
    out = {}
    for kv in filter(None, text.split(",")):
        k, _, v = kv.partition("=")
        if k.strip() not in PHYSICS_DEFAULTS or not v.strip().isdigit():
            raise argparse.ArgumentTypeError(f"bad physics setting {kv!r}; known: {', '.join(PHYSICS_DEFAULTS)}")
        out[k.strip()] = int(v)
    return out


def _print(path, r):
    verdict = "VALID" if r["valid"] else "INVALID"
    print(f"{path}: {verdict}  ({rules.label(r['n'])}, {r['track']} track, {r['mode']} mode, stage: {r['stage']})")
    if r["volume"] is not None:
        w, h, d = r["dims"]
        label = "volume" if r["valid"] else "volume so far"
        print(f"  {label}: {r['volume']} ({w} x {h} x {d}), blocks at rest: {r['block_count']}")
    if r["valid"]:
        print(f"  open: {r['open_ticks']} ticks, close: {r['close_ticks']} ticks, reset: {r['reset_ticks']} ticks")
        if r.get("score") is not None:
            print(f"  score: {r['score']} (reference volume {r['reference_volume']})")
    if "translations" in r:
        t = r["translations"]
        print(f"  shifted and turned placements passed: {t['passed']}/{t['of']}" + (f", failed at offsets {t['failed_offsets']}" if t["failed_offsets"] else ""))
    for f in r["failures"]:
        pos = f" at {f['pos']}" if "pos" in f else ""
        print(f"  FAIL {f['code']}{pos}: {f['message']}")
        if "timeline" in f:
            print("       doorway over time (tick: rows top to bottom): " + ", ".join(f"{t}: {d}" for t, d in f["timeline"]))
        if "cells" in f:
            print("       " + "; ".join(f"{c} is {s}" for c, s in f["cells"]))
    for w in r["warnings"]:
        print(f"  warn {w['code']}: {w['message']} {w.get('positions', '')}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pdgrader", description="Piston-door grader (rulebook v0, Minecraft Java 26.3)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("setup", help="unpack server libraries and compile the simulation kernel")
    s.add_argument("--java-home", required=True, help="a JDK 25 home directory")
    s.add_argument("--server-jar", required=True, help="the Minecraft 26.3 server.jar")
    g = sub.add_parser("grade", help="grade one or more submission JSON files")
    g.add_argument("files", nargs="+")
    g.add_argument("--n", type=_size, required=True, help="door size: 3 for 3x3, or WxH such as 3x2")
    g.add_argument("--track", choices=rules.TRACKS, default="open")
    g.add_argument("--final", action="store_true", help="final mode: more cycles, varied flip timing, fresh simulator per file")
    g.add_argument("--reference", type=int, help="reference volume, to report a score")
    g.add_argument("--translations", action="store_true", help="also report the pass rate at 8 shifted positions")
    g.add_argument("--json", action="store_true", help="print full JSON results")
    g.add_argument("--physics", type=_physics, default={}, help="changed physics, e.g. repeater_unit=3,push_limit=8")
    v = sub.add_parser("serve", help="run the tool server for one agent run")
    v.add_argument("--n", type=_size, required=True, help="door size: 3 for 3x3, or WxH such as 3x2")
    v.add_argument("--track", choices=rules.TRACKS, default="open")
    v.add_argument("--port", type=int, required=True)
    v.add_argument("--host", default="127.0.0.1", help="address to listen on (0.0.0.0 inside a container)")
    v.add_argument("--log", required=True, help="server-side log file (jsonl); keep it out of the agent's reach")
    v.add_argument("--tests", type=int, default=150, help="test-call budget")
    v.add_argument("--sims", type=int, default=400, help="trace/view-call budget")
    v.add_argument("--lab-ticks", type=int, default=50000, help="budget of game ticks advanced in the lab")
    v.add_argument("--minutes", type=int, help="wall-clock limit in minutes, counted from the agent's first tool call (default: none)")
    v.add_argument("--kit", help="also write the agent's working folder here")
    v.add_argument("--physics", type=_physics, default={}, help="changed physics, e.g. repeater_unit=3,push_limit=8")
    v.add_argument("--kit-version", type=int, default=1, choices=(1, 2), help="1: the frozen first-benchmark kit; 2 adds the film and more facts")
    v.add_argument("--resume", action="store_true",
                   help="carry on the run in --log after a restart: budgets and limits come from the log, used calls and time are restored")
    v.add_argument("--variant", choices=("scratch", "improve"), default="scratch",
                   help="improve: hand the agent a working but bulky design to shrink")
    v.add_argument("--starting", help="the design to hand over in the improve variant (default: the task's entry in references.py)")
    v.add_argument("--starting-volume", type=int)
    m = sub.add_parser("serve-many", help="several agent runs in one process sharing one simulator")
    m.add_argument("spec", help='JSON file: a list of {"name", "port", "n", "track", "log", "kit"?, "variant"?, "minutes"?, "budget"?}')
    m.add_argument("--resume", action="store_true", help="carry on every run from its log after a restart (kits are left alone)")
    m.add_argument("--exclude", nargs=2, type=float, action="append", metavar=("START", "END"), default=[],
                   help="with --resume: a wall-clock window (unix seconds) that must not count against any run's time, e.g. the machine asleep")
    c = sub.add_parser("score", help="final verdict for a finished run, from its log")
    c.add_argument("log")
    c.add_argument("--reference", type=int)
    c.add_argument("--out", help="write the result JSON here")
    args = ap.parse_args(argv)

    if args.cmd == "serve":
        from . import kit, references, server
        budget = {"test": args.tests, "sim": args.sims, "lab": args.lab_ticks}
        starting, volume = args.starting, args.starting_volume
        variant = "improve" if starting else args.variant
        if variant == "improve" and not starting:
            starting, volume = references.starting(args.n, args.track)
            if not starting:
                ap.error(f"no starting design is recorded for {rules.label(args.n)} {args.track}; pass --starting")
        if args.resume and args.kit:
            ap.error("--resume keeps the agent's existing folder; leave out --kit")
        if args.kit:
            kit.make_kit(args.kit, args.n, args.track, f"http://127.0.0.1:{args.port}", budget, starting, volume, minutes=args.minutes,
                         physics=args.physics, kit=args.kit_version)
        server.serve(args.n, args.track, args.log, args.port, budget=budget, host=args.host, variant=variant, minutes=args.minutes,
                     resume=args.resume, physics=args.physics, kit=args.kit_version)
        return 0
    if args.cmd == "serve-many":
        from . import kit, references, server
        specs = json.loads(open(args.spec).read())
        for sp in specs:
            sp["n"] = rules.norm(sp["n"])
            sp["budget"] = {**{"test": 150, "sim": 400, "lab": 50000}, **sp.get("budget", {})}
            if sp.get("kit") and not args.resume:
                starting, volume = (None, None)
                if sp.get("variant") == "improve":
                    starting, volume = references.starting(sp["n"], sp["track"])
                kit.make_kit(sp["kit"], sp["n"], sp["track"], f"http://127.0.0.1:{sp['port']}", sp["budget"], starting, volume,
                             minutes=sp.get("minutes"), physics=sp.get("physics"), kit=sp.get("kit_version", 1))
        server.serve_many(specs, resume=args.resume, exclude=args.exclude)
        return 0
    if args.cmd == "score":
        from . import server
        result = server.score(args.log, reference=args.reference)
        if args.out:
            with open(args.out, "w") as f:
                json.dump(result, f, indent=1)
        print(json.dumps({k: v for k, v in result.items() if k != "candidate"}, indent=1))
        return 0 if result["valid"] else 1

    if args.cmd == "setup":
        kernel_mod.setup(args.java_home, args.server_jar)
        print("grader is set up")
        return 0

    mode = "final" if args.final else "dev"
    results, k = {}, None
    try:
        for path in args.files:
            with open(path) as f:
                submission = json.load(f)
            if k is None or args.final:
                if k:
                    k.close()
                k = kernel_mod.Kernel(physics=args.physics)
            results[path] = grade(k, submission, args.n, args.track, mode, reference=args.reference)
            if args.translations and results[path]["valid"]:
                results[path]["translations"] = translation_pass_rate(k, submission, args.n, args.track, mode)
    finally:
        if k:
            k.close()
    if args.json:
        print(json.dumps(results, indent=1))
    else:
        for path, r in results.items():
            _print(path, r)
    return 0 if all(r["valid"] for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
