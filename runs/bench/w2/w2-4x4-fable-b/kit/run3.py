import importlib, sim; importlib.reload(sim)
d = sim.build.build()
lab = Lab(d, walls=True); lab.rest(); t0=lab.t
lab.flip(-3,7,4); lab.step(40)
for t,p,b,a in lab.history:
    if 0<=t-t0<=40 and p[1]>=5 and p[2]>=1 and ('powered=true' in a or 'power=1' in a) and 'power=0' in b+'power=0' :
        if 'wire' in a and not (p in [(-1,7,3),(2,7,3),(4,7,3),(6,7,3),(4,9,3),(0,9,3),(0,5,2),(0,5,4),(-1,6,4),(4,6,4)]): continue
        print(t-t0,p,a[:40])
