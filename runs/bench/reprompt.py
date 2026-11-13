"""Usage: python3 reprompt.py <manifest> <run name>  -> prints the neutral continue message and bumps the run's round count."""
import json, sys, time
man_path, name = sys.argv[1], sys.argv[2]
man = json.load(open(man_path))
run = next(r for r in man["runs"] if r["name"] == name)
log = [json.loads(l) for l in open(run["log"]) if l.strip()]
first = next(e["unix"] for e in log if e["kind"] == "first_call")
windows = [w for e in log if e["kind"] == "resume" for w in e.get("excluded", [])]
now = time.time()
used = (now - first - sum(max(0.0, min(b, now) - max(a, first)) for a, b in windows)) / 60
best = min((e["volume"] for e in log if e["kind"] == "test" and e.get("valid")), default=None)
total = run.get("minutes", man.get("minutes"))
left = total - used
run["rounds"] = run.get("rounds", 1) + 1
run.setdefault("reprompts", []).append({"unix": round(time.time()), "minutes_used": round(used, 1), "best": best})
json.dump(man, open(man_path, "w"), indent=1)
print(f"You stopped with time left: {used:.0f} of {total} minutes used, about {left:.0f} left. "
      f"Your best valid volume so far: {best if best else 'none (no design has passed a test yet)'}.\n\n"
      "Keep working on the task in the same folder until the time is up: build, test and improve your door. "
      "When the time is up, or you have truly done all you can, reply with the same report as before.")
