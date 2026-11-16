import json, glob, collections, os, math
B="/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/"
rows=[]
for f in sorted(glob.glob(B+"w*/*/result.json")):
    r=json.load(open(f)); run=f.split("/")[-2]
    if not r.get("valid"): continue
    cand=r["candidate"]; bl=cand["blocks"]
    c=collections.Counter(b["id"].replace("minecraft:","") for b in bl)
    reps=[b for b in bl if "repeater" in b["id"]]
    delays=collections.Counter(int((b.get("props") or {}).get("delay",1)) for b in reps)
    facing=sum(1 for b in bl if "facing" in (b.get("props") or {}))
    nsite=len(bl)
    rows.append(dict(run=run, n=r["n"], phys=r.get("physics"), kit=r.get("kit"), vol=r["volume"], dims=r["dims"], bc=r["block_count"], nsub=nsite,
        open=r.get("open_ticks"), close=r.get("close_ticks"), secs=r.get("seconds"), init=cand["initial_state"], counts=dict(c), reps=len(reps), delays=dict(delays), facing=facing, transl=r["translations"]["passed"]))
rows.sort(key=lambda x:(str(x['n']), x['vol']))
for x in rows:
    print(f"{x['run']:22s} n={x['n']} phys={x['phys'] or '-'} vol={x['vol']} dims={x['dims']} submitted={x['nsub']} block_count={x['bc']} open={x['open']} close={x['close']} init={x['init']} score_secs={x['secs']} reps={x['reps']} delays={x['delays']} facing_blocks={x['facing']}")
    print("      ", dict(sorted(x['counts'].items(), key=lambda kv:-kv[1])))
json.dump(rows, open("/private/tmp/claude-501/pdnotes/rows.json","w"))
