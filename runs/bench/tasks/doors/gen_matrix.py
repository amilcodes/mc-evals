"""Physics matrix: grade every verified door under each physics variant (dev grade, seamless).

    python3 gen_matrix.py [max_volume]

Output: data/physics_matrix.json  {variant_tag: {run: brief}}. Resumable: variants already in the
file are skipped. Doors bigger than max_volume (default 1500) are skipped to save simulator time.
One kernel at a time.
"""
import json
import sys
import time

import lib

VARIANTS = [
    {},
    lib.CHG,
    {"repeater_unit": 3},
    {"repeater_unit": 1},
    {"observer_delay": 3},
    {"observer_delay": 1},
    {"observer_pulse": 3},
    {"observer_pulse": 1},
    {"push_limit": 8},
]

OUT = lib.HERE / "data/physics_matrix.json"


def main():
    max_vol = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    OUT.parent.mkdir(exist_ok=True)
    mat = json.load(open(OUT)) if OUT.exists() else {}
    ds = [d for d in lib.doors() if d["volume"] <= max_vol]
    for p in VARIANTS:
        tag = lib.phys_tag(p)
        if tag in mat and all(d["run"] in mat[tag] for d in ds):
            continue
        row = mat.setdefault(tag, {})
        t0 = time.monotonic()
        with lib.kernel(p) as k:
            for d in ds:
                if d["run"] in row:
                    continue
                stage, b = lib.grade_ladder(k, d["candidate"], d["n"], final=False)
                row[d["run"]] = {**b, "stage": stage}
        print(f"{tag}: {sum(v['valid'] for v in row.values())}/{len(row)} pass dev, {time.monotonic() - t0:.0f}s", flush=True)
        lib.write_json(OUT, mat)
    lib.cleanup()


if __name__ == "__main__":
    main()
