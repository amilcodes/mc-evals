"""Usage: python3 register.py <manifest> <run name> <agent id>  -> records that the run's agent was launched now."""
import json, sys, time
T = "/private/tmp/claude-501/-Users-AmilAgrawal-Library-Application-Support-Claude-scratch-workspaces-d9080dc0-6400-4a71-ba8b-e896651c820d-d48e81fa-2e2e-421b-9196-f7a0199ec441-scratch-2026-11-09-4800c6/604acb09-bbd6-4e70-8cb0-eae470f68849/tasks/"
path, name, agent = sys.argv[1:4]
m = json.load(open(path))
r = next(x for x in m["runs"] if x["name"] == name)
r.update({"agent": agent, "transcript": T + agent + ".output", "status": "running", "launched_unix": round(time.time())})
json.dump(m, open(path, "w"), indent=1)
print("registered", name)
