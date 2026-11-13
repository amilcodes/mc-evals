from build import *
import time,sys
t0=time.time()
best=None
for (ox,oy,oz,box) in [(-7,0,0,(-8,4,-2,4,-3,3)),(-6,0,0,(-8,4,-2,4,-3,3)),(-7,1,0,(-8,4,-2,4,-3,3)),(-7,0,0,(-8,4,-2,4,-2,2))]:
    ok=0
    for seed in range(25):
        try:
            d,chain,taps=build(ox,oy,oz,swap=False,box=box,seed=seed)
        except Exception as e:
            continue
        ok+=1
        bb=d.bbox(); vol=(bb[1][0]-bb[0][0]+1)*(bb[1][1]-bb[0][1]+1)*(bb[1][2]-bb[0][2]+1)
        if best is None or vol<best[0]:
            best=(vol,(ox,oy,oz,box),seed,bb); print(best,flush=True)
            d.save(f"cand_{vol}.json")
    print((ox,oy,oz),'ok',ok,time.time()-t0,flush=True)
