from pdbuild import Design
# probe A: lever on upper frame block; piston two below (QC) - does it move?
p = Design()
p.set(3,1,0,"stone"); p.set(3,0,0,"stone")
p.set(4,1,0,"lever",face="wall",facing="east")
p.set(3,-1,0,"sticky_piston",facing="west"); p.set(2,-1,0,"stone")
l = Lab(p); print("A lost",l.lost, l.flip(4,1,0)); print(l.step(6))
# probe B: bottom row of three, dust at E pointing east into stone above Q0; does Q1 follow by QC?
p = Design()
for x in range(3):
    p.set(x,-2,0,"sticky_piston",facing="up"); p.set(x,-1,0,"stone")
p.set(-1,-2,0,"stone"); p.set(-1,-1,0,"redstone_wire")
p.set(-2,-2,0,"stone"); p.set(-2,-1,0,"redstone_wire")
p.set(-3,-2,0,"stone"); p.set(-3,-1,0,"lever",face="floor",facing="north")
l = Lab(p); print("B lost",l.lost, l.flip(-3,-1,0))
for c in l.step(8): print(c)
