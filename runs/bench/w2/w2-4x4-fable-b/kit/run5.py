from pdlab import *
import importlib, build2, sim; importlib.reload(build2); importlib.reload(sim)
d = build2.build()
CH=sim.CH
def run(d, flips=1, ticks=70):
    lab = Lab(d, walls=True)
    if lab.lost: print('LOST', lab.lost)
    lab.rest()
    for f in range(flips):
        lab.flip(-3,7,2); t0=lab.t; prev=None
        for i in range(ticks//2):
            lab.step(2); s=sim.snap(lab)
            if s!=prev: print(f'f{f} t{lab.t-t0:3d} {s}')
            prev=s
        lab.rest(); print('rest', lab.doorway(), lab.entity)
    return lab,t0
lab,t0=run(d, 6, 90)
for t,p,b,a in lab.history:
    if p in [(-1,5,1),(-2,4,1),(-2,3,2),(-3,2,2),(-3,2,1),(-2,2,1)] and 0<=t-t0<70: print(t-t0,p,a[13:70])
