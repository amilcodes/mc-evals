import json, math, collections
B="/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/dashboard/"
c=json.load(open(B+"curve.json")); runs={r['run']:r for r in json.load(open(B+"runs.json"))}
by=collections.defaultdict(list)
for p in c: by[p['run']].append(p)
def analyze(names, cutoff=60):
    tot=after=0; rows=[]
    for n in names:
        pts=sorted(by[n], key=lambda p:p['test'])
        vs=[(p['minutes'],p['best']) for p in pts if p['best']]
        if not vs: continue
        first=vs[0][1]; final=runs[n]['volume']; bestcurve=vs[-1][1]
        at=[v for m,v in vs if m<=cutoff]
        v60=at[-1] if at else first
        imp=math.log(first)-math.log(final); a=math.log(v60)-math.log(final)
        tot+=imp; after+=a
        rows.append((n, vs[0][0], first, v60, bestcurve, final, round(imp,3), round(a,3)))
    return rows, tot, after
for label, filt in [("4x4 kit1 (w2,w4)", lambda r: r['task']=="4×4 seamless"), ("4x4 all incl kit2", lambda r: r['task'].startswith("4×4")), ("3x3 standard all", lambda r: r['task']=="3×3 seamless")]:
    names=[n for n,r in runs.items() if filt(r) and r['status']=='door']
    rows,tot,after=analyze(names)
    print(label, len(rows))
    for r in rows: print("  ",r)
    print("  total log-improvement",round(tot,3),"after 60 min",round(after,3),"share",round(after/tot,3) if tot else None)
    # share of improvement measured from first door, but counting time before first door as 'first hour'
