import json, math
rows={r['run']:r for r in json.load(open("/private/tmp/claude-501/pdnotes/rows.json"))}
ROOT="/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/"
D6={"piston","sticky_piston","observer"}; H4={"repeater","comparator","redstone_wall_torch","white_glazed_terracotta"}
for run in ["w1-fable-a","w8-3x3-chg-b-opus","w5-3x3p-fable-a","w5-3x3p-fable-b","w3-opus-d","w4-4x4-opus-e","w2-4x4-fable-a","w2-4x4-opus-b"]:
    c=json.load(open(f"{ROOT}{run.split('-')[0]}/{run}/result.json"))["candidate"]
    ids=[b["id"].replace("minecraft:","") for b in c["blocks"]]
    R=ids.count("repeater"); d6=sum(i in D6 for i in ids); h4=sum(i in H4 for i in ids); comp=ids.count("comparator")
    log_delay=R*math.log10(4); log_face=d6*math.log10(6)+h4*math.log10(4); log_cmp=comp*math.log10(2)
    vol=rows[run]['vol']
    # crude layout space: each bbox cell = air or one of 20 block types (ignoring orientation)
    print(f"{run}: repeaters={R} -> 4^{R} = {4**R if R<30 else '10^%.1f'%log_delay} delay combos; 6-facing blocks={d6}, 4-facing blocks={h4}, comparators={comp}; "
          f"delays+facings+modes = 10^{log_delay+log_face+log_cmp:.1f}; layout (21 choices x {vol} cells) = 10^{vol*math.log10(21):.0f}")
