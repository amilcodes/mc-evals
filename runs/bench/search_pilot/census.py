"""Single-edit census: grade every design one block-edit away from a seed door.

    python3 census.py <run-id> <n> [workers]

Neighbourhood: every cell of the seed's z=0 bounding-box slab except the doorway and the lever,
set to each state in PALETTE other than its current one (air = delete). Edits stay inside the
seed's box, so no neighbour can be larger on paper (pistons can still sweep further). Each
neighbour gets a dev grade (3 cycles, seamless track). Neighbours that pass dev are re-graded
with the final grade (8 cycles, offset flips). Output: census_<run-id>.jsonl, one line each.
"""
import copy
import json
import multiprocessing as mp
import sys
import tempfile as _tf
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCRATCH = Path("/private/tmp/claude-501/census_k")


def palette():
    out = [("air", {}), ("stone", {}), ("redstone_block", {}), ("slime_block", {}), ("honey_block", {}),
           ("obsidian", {}), ("glass", {}), ("target", {}), ("note_block", {}), ("redstone_wire", {}),
           ("redstone_torch", {})]
    d6 = ["north", "south", "east", "west", "up", "down"]
    h4 = d6[:4]
    out += [("piston", {"facing": f}) for f in d6] + [("sticky_piston", {"facing": f}) for f in d6]
    out += [("observer", {"facing": f}) for f in d6]
    out += [("repeater", {"facing": f, "delay": str(d)}) for f in h4 for d in range(1, 5)]
    out += [("comparator", {"facing": f, "mode": m}) for f in h4 for m in ("compare", "subtract")]
    out += [("redstone_wall_torch", {"facing": f}) for f in h4]
    return out


PALETTE = palette()


def norm(b):
    bid = b["id"].split(":")[-1]
    p = {k: str(v) for k, v in (b.get("props") or {}).items()}
    if bid == "redstone_wire":
        p = {}                      # wire shape is recomputed by the game
    if bid == "repeater":
        p = {"facing": p.get("facing", "north"), "delay": p.get("delay", "1")}
    if bid in ("piston", "sticky_piston", "observer"):
        p = {"facing": p.get("facing", "north")}
    if bid == "comparator":
        p = {"facing": p.get("facing", "north"), "mode": p.get("mode", "compare")}
    if bid == "redstone_wall_torch":
        p = {"facing": p.get("facing", "north")}
    return bid, p


def neighbours(seed, n):
    from pdgrader import rules
    cells = {tuple(b["pos"]): i for i, b in enumerate(seed["blocks"])}
    lever = next(tuple(b["pos"]) for b in seed["blocks"] if b["id"].endswith("lever"))
    body = [p for p in cells if p != lever]
    lo = [min([p[i] for p in body] + [0]) for i in range(3)]
    hi = [max([p[i] for p in body] + [n - 1, n - 1, 0][i:i + 1]) for i in range(3)]
    out = []
    for x in range(lo[0], hi[0] + 1):
        for y in range(lo[1], hi[1] + 1):
            for z in range(lo[2], hi[2] + 1):
                pos = (x, y, z)
                if pos == lever or rules.in_doorway(n, pos) or rules.in_hallway(n, pos) or rules.in_shell(n, pos):
                    continue
                cur = norm(seed["blocks"][cells[pos]]) if pos in cells else ("air", {})
                for bid, props in PALETTE:
                    if (bid, props) == cur:
                        continue
                    out.append({"pos": list(pos), "from": [cur[0], cur[1]], "to": [bid, props]})
    return out


def apply(seed, edit):
    s = copy.deepcopy(seed)
    pos = edit["pos"]
    s["blocks"] = [b for b in s["blocks"] if b["pos"] != pos]
    bid, props = edit["to"]
    if bid != "air":
        s["blocks"].append({"pos": list(pos), "id": bid, **({"props": dict(props)} if props else {})})
    return s


def brief(r):
    out = {k: r.get(k) for k in ("valid", "volume", "open_ticks", "close_ticks", "reset_ticks", "flips_passed", "partial", "block_count")}
    out["fail"] = r["failures"][0]["code"] if r["failures"] else None
    return out


def worker(args):
    wid, run, n, seed, edits, physics, outq = args
    sys.path.insert(0, str(ROOT / "grader"))
    import pdgrader.kernel as K
    from pdgrader.grade import grade
    SCRATCH.mkdir(parents=True, exist_ok=True)
    K.tempfile = types.SimpleNamespace(mkdtemp=lambda prefix="", dir=None: _tf.mkdtemp(prefix=prefix, dir=str(SCRATCH)))
    with K.Kernel(heap="1500M", physics=physics) as k:
        for e in edits:
            s = apply(seed, e)
            t = time.monotonic()
            try:
                r = grade(k, s, n, "seamless", "dev")
                rec = {**e, "dev": brief(r)}
                if r["valid"]:
                    rec["final"] = brief(grade(k, s, n, "seamless", "final"))
            except Exception as ex:  # a kernel hiccup must not kill the census
                rec = {**e, "error": repr(ex)[:200]}
            rec["wall"] = round(time.monotonic() - t, 3)
            outq.put(rec)
    outq.put(("done", wid))


def main():
    run, n = sys.argv[1], int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    physics = json.loads(sys.argv[4]) if len(sys.argv) > 4 else None
    sys.path.insert(0, str(ROOT / "grader"))
    wave = run.split("-")[0]
    seed = json.load(open(ROOT / f"runs/bench/{wave}/{run}/result.json"))["candidate"]
    edits = neighbours(seed, n)
    tag = run + ("" if not physics else "_" + "_".join(f"{k}{v}" for k, v in sorted(physics.items())))
    out = HERE / f"census_{tag}.jsonl"
    done = set()
    if out.exists():
        for line in open(out):
            r = json.loads(line)
            done.add((tuple(r["pos"]), json.dumps(r["to"], sort_keys=True)))
    todo = [e for e in edits if (tuple(e["pos"]), json.dumps(e["to"], sort_keys=True)) not in done]
    print(f"{run}: {len(edits)} neighbours, {len(todo)} to grade, {workers} workers", flush=True)
    if not todo:
        return
    mgr = mp.Manager()
    q = mgr.Queue()
    chunks = [todo[i::workers] for i in range(workers)]
    pool = mp.Pool(workers)
    pool.map_async(worker, [(i, run, n, seed, chunks[i], physics, q) for i in range(workers)])
    t0, finished, count, valid = time.monotonic(), 0, 0, 0
    with open(out, "a") as f:
        while finished < workers:
            r = q.get()
            if isinstance(r, tuple):
                finished += 1
                continue
            f.write(json.dumps(r) + "\n")
            f.flush()
            count += 1
            valid += bool(r.get("dev", {}).get("valid"))
            if count % 200 == 0:
                el = time.monotonic() - t0
                print(f"{count}/{len(todo)} graded, {valid} valid, {el:.0f}s, eta {el / count * (len(todo) - count):.0f}s", flush=True)
    pool.close()
    pool.join()
    print(f"done: {count} graded, {valid} pass dev, {time.monotonic() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
