from pdbuild import Design
d=Design("open")
for y in (0,1):
    d.set(-2,y,0,"sticky_piston",facing="east"); d.set(3,y,0,"sticky_piston",facing="west")
    d.set(-1,y,0,"stone"); d.set(2,y,0,"stone")
for x in (0,1):
    d.set(x,2,0,"stone"); d.set(x,-1,0,"stone")
for x in (-2,-1,2,3): d.set(x,2,0,"stone")
for x in range(-2,4): d.set(x,3,0,"redstone_wire")
d.set(-3,2,0,"lever",face="wall",facing="west")
d.save("g1.json")
