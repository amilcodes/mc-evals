from build import *
import time,sys
t0=time.time()
best=None
cfgs=[]
for oz in (-2,-1):
  for oy in (6,):
    for box in [(-3,4,-3,7,-2,2),(-4,5,-3,7,-3,3),(-3,4,-3,7,-3,3)]:
        cfgs.append((0,oy,oz,box))
for (ox,oy,oz,box) in cfgs:
    ok=0
    for seed in range(40):
        try:
            d,chain,taps=build(ox,oy,oz,swap=True,box=box,seed=seed)
        except Exception as e:
            continue
        ok+=1
        bb=d.bbox(); vol=(bb[1][0]-bb[0][0]+1)*(bb[1][1]-bb[0][1]+1)*(bb[1][2]-bb[0][2]+1)
        if best is None or vol<best[0]:
            best=(vol,(ox,oy,oz,box),seed,bb); print(best,flush=True)
            d.save(f"cand_{vol}.json")
    print((ox,oy,oz,box),'ok',ok,round(time.time()-t0),flush=True)
