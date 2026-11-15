"""Usage: python3 finish.py <manifest> <run name> [note]  -> marks a run finished (continue cap reached or time up)."""
import json, sys
path, name = sys.argv[1:3]
m = json.load(open(path))
r = next(x for x in m["runs"] if x["name"] == name)
r["status"] = "finished: " + (sys.argv[3] if len(sys.argv) > 3 else "stopped after the third continue message")
json.dump(m, open(path, "w"), indent=1)
print(name, "->", r["status"], "| rounds", r.get("rounds", 1))
