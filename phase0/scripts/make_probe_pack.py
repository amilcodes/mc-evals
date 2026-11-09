#!/usr/bin/env python3
"""Build a datapack of probe game tests for the vanilla headless test runner.

Usage: make_probe_pack.py <packs_dir> <copies>

Creates <packs_dir>/probe/ containing three block-based tests:
  pd:dust_pass    start block -> redstone dust -> accept block
  pd:piston_pass  start block -> piston pushes stone -> observer -> accept block
  pd:never_fail   start block with nothing connected to accept (expected to time out)
plus <copies> extra instances of piston_pass (pd:bulk/pNNNN) to measure per-test cost.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nbt_structure import write_structure  # noqa: E402

DATA_VERSION = 5023  # Minecraft Java 26.3
PACK_FORMAT = 121


def test_block(x, mode):
    return {
        "pos": [x, 1, 0],
        "id": "minecraft:test_block",
        "props": {"mode": mode},
        "nbt": {"id": "minecraft:test_block", "mode": mode, "message": ""},
    }


def floor(n):
    return [{"pos": [x, 0, 0], "id": "minecraft:stone"} for x in range(n)]


def wire(x):
    return {
        "pos": [x, 1, 0],
        "id": "minecraft:redstone_wire",
        "props": {"east": "side", "west": "side", "north": "none", "south": "none", "power": 0},
    }


STRUCTURES = {
    "dust_pass": floor(4) + [test_block(0, "start"), wire(1), wire(2), test_block(3, "accept")],
    "piston_pass": floor(6)
    + [
        test_block(0, "start"),
        {"pos": [1, 1, 0], "id": "minecraft:piston", "props": {"facing": "east", "extended": "false"}},
        {"pos": [2, 1, 0], "id": "minecraft:stone"},
        {"pos": [4, 1, 0], "id": "minecraft:observer", "props": {"facing": "west", "powered": "false"}},
        test_block(5, "accept"),
    ],
    "never_fail": floor(4) + [test_block(0, "start"), test_block(3, "accept")],
}
SIZES = {"dust_pass": [4, 2, 1], "piston_pass": [6, 2, 1], "never_fail": [4, 2, 1]}


def instance(structure, max_ticks=40):
    return {
        "type": "minecraft:block_based",
        "environment": "minecraft:default",
        "structure": f"pd:{structure}",
        "max_ticks": max_ticks,
        "setup_ticks": 0,
        "required": True,
    }


def main():
    packs, copies = Path(sys.argv[1]), int(sys.argv[2])
    pack = packs / "probe"
    if pack.exists():
        shutil.rmtree(pack)
    sdir = pack / "data" / "pd" / "structure"
    tdir = pack / "data" / "pd" / "test_instance"
    (tdir / "bulk").mkdir(parents=True)
    sdir.mkdir(parents=True)
    (pack / "pack.mcmeta").write_text(
        json.dumps({"pack": {"description": "piston door probe tests", "min_format": PACK_FORMAT, "max_format": PACK_FORMAT}})
    )
    for name, blocks in STRUCTURES.items():
        write_structure(sdir / f"{name}.nbt", blocks, DATA_VERSION, SIZES[name])
        (tdir / f"{name}.json").write_text(json.dumps(instance(name)))
    for i in range(copies):
        (tdir / "bulk" / f"p{i:04d}.json").write_text(json.dumps(instance("piston_pass")))
    print(f"wrote {pack} with {3 + copies} test instances")


if __name__ == "__main__":
    main()
