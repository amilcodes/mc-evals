"""Writes the pdcheck datapack into server/world: function pdcheck:diff says every cell in and around the
door's swept box that differs from the film's start state (walls and the lever excluded)."""
import json, os
f = json.load(open("../opus_5236_film.json"))
lo, hi = f["swept_box"]["min"], f["swept_box"]["max"]
start = {(x, y, z): s for x, y, z, s in f["start"]["blocks"]}
walls = {tuple(w) for w in f["walls"]}
lines = []
for x in range(lo[0] - 3, hi[0] + 4):
    for y in range(lo[1] - 3, hi[1] + 4):
        for z in range(min(lo[2], -9) - 2, max(hi[2], 6) + 3):
            if (x, y, z) == tuple(f["lever"]):
                continue
            s = "stone" if (x, y, z) in walls else start.get((x, y, z), "air")
            W = (x + 16, y + 103, z + 9)
            lines.append(f"execute unless block {W[0]} {W[1]} {W[2]} minecraft:{s} run say DIFF {W[0]} {W[1]} {W[2]} want {s}")
d = "server/world/datapacks/pdcheck/data/pdcheck/function"
os.makedirs(d, exist_ok=True)
open(d + "/diff.mcfunction", "w").write("\n".join(lines) + "\nsay DIFFDONE\n")
open("server/world/datapacks/pdcheck/pack.mcmeta", "w").write(open("server/world/datapacks/pdcam/pack.mcmeta").read())
print(len(lines), "cells")
