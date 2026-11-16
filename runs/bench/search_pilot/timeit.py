import sys, json, time, types, tempfile as _tf, itertools, copy
ROOT="/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/"
sys.path.insert(0, ROOT+"grader")
import pdgrader.kernel as K
from pdgrader.grade import grade, build_job
from pdgrader import rules
from pdgrader.validate import validate
# keep simulator scratch worlds out of the project folder
K.tempfile = types.SimpleNamespace(mkdtemp=lambda prefix="", dir=None: _tf.mkdtemp(prefix=prefix, dir="/private/tmp/claude-501/pdnotes/k"))
def cand(run):
    w=run.split("-")[0]
    return json.load(open(f"{ROOT}runs/bench/{w}/{run}/result.json"))["candidate"]
D={r:cand(r) for r in ["w1-fable-a","w8-3x3-chg-b-opus","w3-opus-d","w4-4x4-opus-e","w2-4x4-fable-a","w2-4x4-opus-b"]}
N={"w1-fable-a":3,"w8-3x3-chg-b-opus":3,"w3-opus-d":3,"w4-4x4-opus-e":4,"w2-4x4-fable-a":4,"w2-4x4-opus-b":4}
def ticks(k, sub, n, mode):
    errs, blocks = validate(sub, n)
    lever = next(p for p,(b,_) in blocks.items() if b=="minecraft:lever")
    t0=time.monotonic(); res=k.run_job(build_job(n, blocks, lever, mode, rules.TIME_CAP)); dt=time.monotonic()-t0
    return sum(s.get("ticks",0) for s in res["steps"])+100, dt   # +100: clear() drains 100 ticks
def brief(r): return {k:r.get(k) for k in ("valid","volume","open_ticks","close_ticks","reset_ticks","sim_seconds")} | ({"fail":[f["code"]+": "+f["message"][:160] for f in r["failures"]]} if not r["valid"] else {})
out={}
def section(physics):
    tag=json.dumps(physics or "vanilla"); out[tag]={}
    t0=time.monotonic()
    with K.Kernel(physics=physics) as k:
        out[tag]["boot_s"]=k.boot_seconds
        for run,sub in D.items():
            n=N[run]
            if physics and n==4: continue
            rec={}
            # warm-up + repeated dev grades
            ws=[]
            for i in range(4):
                t=time.monotonic(); r=grade(k, sub, n, "seamless", "dev"); ws.append(round(time.monotonic()-t,3))
            rec["dev"]=brief(r); rec["dev_wall_s"]=ws
            t=time.monotonic(); rf=grade(k, sub, n, "seamless", "final"); rec["final"]=brief(rf); rec["final_wall_s"]=round(time.monotonic()-t,3)
            rec["dev_ticks"],_=ticks(k,sub,n,"dev"); rec["final_ticks"],_=ticks(k,sub,n,"final")
            if not physics and run in ("w1-fable-a","w4-4x4-opus-e"):
                t=time.monotonic(); from pdgrader.grade import translation_pass_rate
                tr=translation_pass_rate(k, sub, n, "seamless", "final"); rec["translations"]=tr["passed"]; rec["translations_wall_s"]=round(time.monotonic()-t,2)
            out[tag][run]=rec
            print(tag, run, json.dumps(rec), flush=True)
        if not physics or physics=={"repeater_unit":3,"observer_delay":3}:
            # repeater-delay sweep demo on the two 70-volume doors
            for run in ("w1-fable-a","w8-3x3-chg-b-opus"):
                sub=D[run]; idx=[i for i,b in enumerate(sub["blocks"]) if "repeater" in b["id"]]
                res=[]; t=time.monotonic()
                for combo in itertools.product([1,2,3,4], repeat=len(idx)):
                    s=copy.deepcopy(sub)
                    for i,d in zip(idx,combo): s["blocks"][i].setdefault("props",{})["delay"]=str(d)
                    r=grade(k, s, 3, "seamless", "dev"); res.append([list(combo), r["valid"], r.get("open_ticks"), r.get("close_ticks"), (r["failures"][0]["code"] if r["failures"] else None)])
                el=time.monotonic()-t
                out[tag]["sweep_"+run]={"orig":[sub["blocks"][i].get("props",{}).get("delay","1") for i in idx],"results":res,"wall_s":round(el,2),"per_eval_s":round(el/len(res),3)}
                print(tag,"sweep",run,json.dumps(out[tag]["sweep_"+run]),flush=True)
    out[tag]["section_wall_s"]=round(time.monotonic()-t0,2)
for ph in [None, {"repeater_unit":3,"observer_delay":3}, {"repeater_unit":3}, {"observer_delay":3}]:
    section(ph)
json.dump(out, open("/private/tmp/claude-501/pdnotes/timing.json","w"), indent=1)
print("DONE")
