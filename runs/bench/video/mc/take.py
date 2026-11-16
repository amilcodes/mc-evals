"""One take: fresh copy of the world, launch the client, record ONLY its window from the moment the
player joins (the camera datapack runs its timeline from there), then quit the game."""
import os, shutil, subprocess, sys, time
from pathlib import Path
H = Path(__file__).resolve().parent
R = "/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-10-02-00aea5/rsg-agent"
SECONDS = int(os.environ.get("TAKE_SECONDS", 42))
world = H / "client/saves/PistonDoorBench"
shutil.rmtree(world, ignore_errors=True)
shutil.copytree(H / "server/world", world)
(world / "session.lock").unlink(missing_ok=True)
log = H / "client.log"
log.unlink(missing_ok=True)
pid = int(subprocess.check_output([sys.executable, str(H / "launch_client.py")], text=True).strip())
print("game pid", pid, flush=True)
end = time.time() + 180
while time.time() < end:
    if log.exists() and "joined the game" in log.read_text(errors="ignore"):
        break
    time.sleep(0.25)
else:
    sys.exit("the player never joined")
print("joined; recording", SECONDS, "s", flush=True)
r = subprocess.run([f"{R}/.venv/bin/python", "-m", "rsg.live.terminal", "--timeout", str(SECONDS + 60), "--jobs", str(H / "jobs"), "--",
                    str(H / "WindowRecorder"), str(pid), str(SECONDS), str(H / os.environ.get("TAKE_OUT", "take_raw.mp4")), "60"], cwd=R, capture_output=True, text=True)
print(r.stdout[-400:], r.stderr[-400:], flush=True)
os.kill(pid, 15)
print("game stopped", flush=True)
