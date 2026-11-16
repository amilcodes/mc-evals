"""Boots the 26.3 server on the prepared world, places the door, cycles the lever twice with commands,
checks the doorway after each flip, saves and stops."""
import subprocess, threading, queue, time, sys, re
JAVA = "/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/toolchain/jdk-25.0.5+8/Contents/Home/bin/java"
JAR = "/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/phase0/dl/server/server.jar"
p = subprocess.Popen([JAVA, "-Xmx2G", "-jar", JAR, "nogui"], cwd="server", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
q = queue.Queue()
threading.Thread(target=lambda: [q.put(l.rstrip()) for l in p.stdout], daemon=True).start()
log = []
def drain(t=0.5):
    end = time.time() + t
    out = []
    while time.time() < end:
        try:
            l = q.get(timeout=max(0.01, end - time.time())); out.append(l); log.append(l)
        except queue.Empty:
            pass
    return out
def wait_for(pat, t=180):
    end = time.time() + t
    while time.time() < end:
        try:
            l = q.get(timeout=1); log.append(l)
            if re.search(pat, l): return l
        except queue.Empty:
            pass
    raise SystemExit("timeout waiting for " + pat + "\n" + "\n".join(log[-30:]))
def cmd(c, t=1.0):
    p.stdin.write(c + "\n"); p.stdin.flush()
    return [l.split("]: ", 1)[-1] for l in drain(t)]
wait_for(r"Done \(")
print("server up")
print(cmd("datapack list", 1.5))
print(cmd("forceload add -16 -16 40 32", 3))
DOOR = [(16 + x, 103 + y, 9) for y in range(4) for x in range(4)]
def doorway():
    s = ""
    for y in range(3, -1, -1):
        for x in range(4):
            r = cmd(f"execute if block {16 + x} {103 + y} 9 minecraft:stone", 0.15)
            s += "#" if any("passed" in l for l in r) else "."
        s += "/"
    return s[:-1]
time.sleep(3); drain(0.2)
print("on boot:", doorway())
L = "setblock 0 109 11 minecraft:lever[face=wall,facing=west,powered={}]"
ON = [L.format("true"), "setblock 1 109 11 minecraft:redstone_block"]
OFF = [L.format("false"), "setblock 1 109 11 minecraft:stone"]
for i in range(2):
    for c in ON: cmd(c, 0.1)
    time.sleep(7); print(f"cycle {i+1} lever on :", doorway())
    for c in OFF: cmd(c, 0.1)
    time.sleep(9); print(f"cycle {i+1} lever off:", doorway())
print(cmd("setworldspawn 18 101 -6", 0.5))
print(cmd("save-all flush", 3))
cmd("stop", 0.5)
p.wait(timeout=60)
print("stopped", p.returncode)
