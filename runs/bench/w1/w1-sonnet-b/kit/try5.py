from build import *
import time,sys
t0=time.time()
best=None
cfgs=[]
for oz in (-2,-3):
    for box in [(-3,4,-2,4,-3,3),(-4,5,-2,4,-3,3)]:
        cfgs.append((0,-3,oz,box))
for (ox,oy,oz,box) in cfgs:
    ok=0
    for seed in range(4):
        try:
            d,chain,taps=build(ox,oy,oz,swap=True,box=box,seed=seed,TL=10)
        except Exception as e:
            print('fail',seed,e,flush=True); continue
        ok+=1
        bb=d.bbox(); vol=(bb[1][0]-bb[0][0]+1)*(bb[1][1]-bb[0][1]+1)*(bb[1][2]-bb[0][2]+1)
        if best is None or vol<best[0]:
            best=(vol,(ox,oy,oz,box),seed,bb); print(best,flush=True)
            d.save(f"candB_{vol}.json")
    print((ox,oy,oz,box),'ok',ok,round(time.time()-t0),flush=True)
