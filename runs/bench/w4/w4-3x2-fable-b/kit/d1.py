from pdbuild import Design
d = Design("open")
S="stone"
# frame sides
for y in (0,1):
    d.set(-1,y,0,S); d.set(3,y,0,S)
for x in range(3):
    d.set(x,2,0,S); d.set(x,-1,0,S)
    d.set(x,3,0,"sticky_piston",facing="down")
    d.set(x,-2,0,"sticky_piston",facing="up")
    d.set(x,4,0,"redstone_wire")
# bottom
d.set(2,-3,0,S)
d.set(1,-3,0,"lever",face="wall",facing="west")
d.set(0,-3,0,"observer",facing="east")
d.set(-1,-3,0,S)
d.set(-1,-2,0,"redstone_wire")
d.set(-2,-2,0,S)
d.set(-2,-1,0,"redstone_wire")
d.set(-2,0,0,"observer",facing="down")
d.set(-2,1,0,S)
d.set(-2,2,0,"redstone_wire")
d.set(-1,2,0,S)
d.set(-1,3,0,"redstone_wire")
d.save("d1.json")
