"""Downloads what the 26.3 client needs from Mojang's own URLs (as listed in the version JSON the
launcher saved), into ./client-files, checking every SHA-1. Sound files are skipped."""
import hashlib, json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
MC = Path.home() / "Library/Application Support/minecraft"
OUT = Path("client-files").resolve()
v = json.loads((MC / "versions/26.3/26.3.json").read_text())
def ok(rules):
    if not rules: return True
    allow = False
    for r in rules:
        if "features" in r: continue
        o = r.get("os") or {}
        if (not o or o.get("name") in (None, "osx")) and o.get("arch") in (None, "arm64", "aarch64"):
            allow = r["action"] == "allow"
    return allow
jobs = [(v["downloads"]["client"]["url"], v["downloads"]["client"]["sha1"], OUT / "versions/26.3/26.3.jar")]
for l in v["libraries"]:
    if ok(l.get("rules")):
        a = l["downloads"]["artifact"]
        jobs.append((a["url"], a["sha1"], OUT / "libraries" / a["path"]))
ai = v["assetIndex"]
idx_path = OUT / "assets/indexes" / f"{ai['id']}.json"
jobs.append((ai["url"], ai["sha1"], idx_path))
def get(job):
    url, sha, path = job
    if path.exists() and hashlib.sha1(path.read_bytes()).hexdigest() == sha:
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "minecraft-launcher-files-fetch"})
    data = urllib.request.urlopen(req, timeout=120).read()
    if hashlib.sha1(data).hexdigest() != sha:
        raise SystemExit(f"bad sha1 for {url}")
    path.write_bytes(data)
    return len(data)
with ThreadPoolExecutor(8) as ex:
    got = sum(ex.map(get, jobs))
print(f"client jar + {len(jobs) - 2} libraries + asset index: {got / 1e6:.1f} MB downloaded")
idx = json.loads(idx_path.read_text())
objs = [(k, o) for k, o in idx["objects"].items() if not k.endswith(".ogg")]
ajobs = [(f"https://resources.download.minecraft.net/{o['hash'][:2]}/{o['hash']}", o["hash"], OUT / "assets/objects" / o["hash"][:2] / o["hash"]) for k, o in objs]
with ThreadPoolExecutor(16) as ex:
    got = sum(ex.map(get, ajobs))
print(f"{len(ajobs)} non-sound asset objects ({sum(o['size'] for _, o in objs) / 1e6:.0f} MB), {got / 1e6:.1f} MB downloaded")
