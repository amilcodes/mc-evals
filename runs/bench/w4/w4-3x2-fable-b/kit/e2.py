from pdbuild import Design
import random
d = Design.load("d3.json")
lab = Lab(d, walls=True)
random.seed(1)
ok=True
for i in range(40):
    lab.flip(-2,2,1)
    r = lab.rest()
    lab.step(random.choice([1,2,3,5,7,11,13]))
    want = "###/###" if i%2==0 else ".../..."
    if lab.doorway()!=want or not r or lab.entity: ok=False; print("BAD",i,lab.doorway(),r,lab.entity)
print("ok",ok,lab.t)
# probe: lever on top of a down piston, QC to neighbours
p = Design()
for x in range(3):
    p.set(x,10,0,"sticky_piston",facing="down"); p.set(x,9,0,"stone")
p.set(1,11,0,"lever",face="floor",facing="north")
l2 = Lab(p); print("lost",l2.lost); print(l2.flip(1,11,0))
for c in l2.step(6): print(c)
