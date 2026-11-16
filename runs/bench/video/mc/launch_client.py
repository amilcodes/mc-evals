"""Starts the Minecraft 26.3 client straight into the PistonDoorBench world, the way the official
launcher would for this version, in offline singleplayer mode (no account, no credentials), with
its own game folder ./client and the files fetched into ./client-files.

    python3 launch_client.py [--dry-run]
"""
import json
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
MC = Path.home() / "Library/Application Support/minecraft"
FILES = HERE / "client-files"
GAME = HERE / "client"
JAVA = MC / "runtime/java-runtime-epsilon/mac-os-arm64/jre.bundle/Contents/Home/bin/java"
WORLD = "PistonDoorBench"
WIDTH, HEIGHT = 1600, 900
NAME = "Bench"


def ok(rules):
    if not rules:
        return True
    allow = False
    for r in rules:
        if "features" in r:
            continue
        o = r.get("os") or {}
        if (not o or o.get("name") in (None, "osx")) and o.get("arch") in (None, "arm64", "aarch64"):
            allow = r["action"] == "allow"
    return allow


def build():
    v = json.loads((MC / "versions/26.3/26.3.json").read_text())
    cp = [str(FILES / "libraries" / l["downloads"]["artifact"]["path"]) for l in v["libraries"] if ok(l.get("rules"))]
    cp.append(str(FILES / "versions/26.3/26.3.jar"))
    natives = GAME / ".natives"
    for d in ("java", "jna", "lwjgl", "netty"):
        (natives / d).mkdir(parents=True, exist_ok=True)
    subs = {
        "${natives_directory}": str(natives), "${launcher_name}": "pdbench-recorder", "${launcher_version}": "1",
        "${classpath}": ":".join(cp), "${auth_player_name}": NAME, "${version_name}": "26.3", "${game_directory}": str(GAME),
        "${assets_root}": str(FILES / "assets"), "${assets_index_name}": v["assetIndex"]["id"],
        "${auth_uuid}": str(uuid.uuid3(uuid.NAMESPACE_DNS, "OfflinePlayer:" + NAME)), "${auth_access_token}": "0",
        "${clientid}": "", "${auth_xuid}": "", "${version_type}": "release", "${user_type}": "legacy",
    }

    def expand(items):
        out = []
        for a in items:
            if isinstance(a, dict):
                if not ok(a.get("rules")):
                    continue
                vals = a["value"] if isinstance(a["value"], list) else [a["value"]]
            else:
                vals = [a]
            for s in vals:
                for k, val in subs.items():
                    s = s.replace(k, val)
                out.append(s)
        return out

    jvm = ["-Xmx3G", "-XX:+UseG1GC", *expand(v["arguments"]["jvm"])]
    game = expand(v["arguments"]["game"])
    return [str(JAVA), *jvm, v["mainClass"], *game, "--width", str(WIDTH), "--height", str(HEIGHT), "--quickPlaySingleplayer", WORLD]


def options():
    """Settings for a clean recording: no pause on focus loss, no onboarding, no sound."""
    opts = GAME / "options.txt"
    if opts.exists():
        return
    opts.write_text("\n".join([
        "pauseOnLostFocus:false", "onboardAccessibility:false", "skipMultiplayerWarning:true", "tutorialStep:none",
        "joinedFirstServer:true", "narrator:0", "renderDistance:10", "simulationDistance:8", "maxFps:60", "enableVsync:true",
        "guiScale:2", "fov:0.0", "soundCategory_master:0.0", "fullscreen:false", "renderClouds:\"false\"",
    ]) + "\n")


if __name__ == "__main__":
    GAME.mkdir(exist_ok=True)
    options()
    cmd = build()
    missing = [p for p in cmd[cmd.index("-cp") + 1].split(":") if not Path(p).exists()]
    if missing:
        sys.exit(f"missing files: {missing[:3]}")
    if "--dry-run" in sys.argv:
        print(" ".join(cmd[:8]), "...", " ".join(cmd[-10:]))
        sys.exit(0)
    log = open(HERE / "client.log", "w")
    p = subprocess.Popen(cmd, cwd=GAME, stdout=log, stderr=subprocess.STDOUT)
    print(p.pid)
