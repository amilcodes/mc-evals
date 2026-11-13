from build import *
import time,sys
t0=time.time()
best=None
box=(-3,4,-2,4,-2,2)
for (ox,oy,oz) in [(0,-3,-2),(0,-3,-1)]:
    ok=0
    for seed in range(30):
        try:
            d,chain,taps=build(ox,oy,oz,swap=True,box=box,seed=seed)
        except Exception as e:
            continue
        ok+=1
        bb=d.bbox(); vol=(bb[1][0]-bb[0][0]+1)*(bb[1][1]-bb[0][1]+1)*(bb[1][2]-bb[0][2]+1)
        if best is None or vol<best[0]:
            best=(vol,(ox,oy,oz),seed,bb); print(best,flush=True)
            d.save(f"cand_{vol}.json")
    print((ox,oy,oz),'ok',ok,time.time()-t0,flush=True)
