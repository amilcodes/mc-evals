import sys, json, types, tempfile as _tf, copy, time
ROOT="/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/"
sys.path.insert(0, ROOT+"grader")
import pdgrader.kernel as K
from pdgrader.grade import grade, translation_pass_rate
K.tempfile = types.SimpleNamespace(mkdtemp=lambda prefix="", dir=None: _tf.mkdtemp(prefix=prefix, dir="/private/tmp/claude-501/pdnotes/k"))
sub=json.load(open(ROOT+"runs/bench/w1/w1-fable-a/result.json"))["candidate"]
idx=[i for i,b in enumerate(sub["blocks"]) if "repeater" in b["id"]]
print([ (sub["blocks"][i]["pos"], sub["blocks"][i].get("props")) for i in idx])
with K.Kernel() as k:
    for combo in [(4,2),(4,3),(4,4)]:
        s=copy.deepcopy(sub)
        for i,d in zip(idx,combo): s["blocks"][i]["props"]["delay"]=str(d)
        t=time.monotonic(); r=grade(k,s,3,"seamless","final"); tr=translation_pass_rate(k,s,3,"seamless","final")
        print(combo, r["valid"], r["volume"], r.get("open_ticks"), r.get("close_ticks"), r.get("reset_ticks"), "placements", tr["passed"], "/", tr["of"], round(time.monotonic()-t,2),"s")
