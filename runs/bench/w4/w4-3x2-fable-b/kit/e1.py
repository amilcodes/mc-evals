# probe: 6x6 idea - can a lever mounted on an observer / piston drive anything extra? and does P2 next to powered P1 ever move?
from pdbuild import Design
d = Design("open")
S="stone"
for x in (1,2):
    d.set(x,2,0,S); d.set(x,3,0,"sticky_piston",facing="down")
d.set(0,2,0,S); d.set(0,3,0,"redstone_wire"); d.set(-1,2,0,S); d.set(-1,3,0,"redstone_wire")
d.set(-2,3,0,S); d.set(-2,4,0,"lever",face="floor",facing="north")
d.set(3,3,0,"observer",facing="west"); 
lab = Lab(d)
print(lab.lost)
print(lab.flip(-2,4,0)); 
for c in lab.step(12): print(c)
