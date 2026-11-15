from pdbuild import Design
d=Design("open")
for x in range(3):
    d.set(x,-1,0,"stone"); d.set(x,2,0,"stone")
for y in range(2):
    d.set(-1,y,0,"stone"); d.set(3,y,0,"stone")
d.set(-2,0,0,"sticky_piston",facing="east")
for x in (1,2): d.set(x,-2,0,"sticky_piston",facing="up")
for x in range(3):
    d.set(x,3,0,"sticky_piston",facing="down"); d.set(x,4,0,"redstone_wire")
d.set(-2,-2,0,"stone"); d.set(-2,-1,0,"lever",face="floor",facing="north")
d.set(-1,-1,0,"observer",facing="west")
d.set(-1,-2,0,"observer",facing="up")
d.set(0,-2,0,"observer",facing="west")
for y in (1,2,3): d.set(-2,y,0,"observer",facing="down")
d.set(-2,4,0,"redstone_wire"); d.set(-1,3,0,"stone"); d.set(-1,4,0,"redstone_wire")
d.set(3,3,0,"stone"); d.set(3,4,0,"redstone_wire"); d.set(4,4,0,"redstone_wire")
for y in range(-2,4): d.set(4,y,0,"observer",facing="up")
d.set(3,-2,0,"observer",facing="east")
d.save("w/v4.json")
