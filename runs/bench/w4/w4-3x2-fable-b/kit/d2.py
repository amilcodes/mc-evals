from pdbuild import Design
d = Design("open")
S="stone"
for x in (0,2):
    d.set(x,2,0,S); d.set(x,-1,0,S)
d.set(1,2,0,S); d.set(1,-1,0,S)
d.set(1,3,0,"sticky_piston",facing="down")
d.set(1,-2,0,"sticky_piston",facing="up")
for y in (0,1):
    d.set(-1,y,0,S); d.set(3,y,0,S)
    d.set(-2,y,0,"sticky_piston",facing="east")
    d.set(4,y,0,"sticky_piston",facing="west")
d.set(1,3,1,"lever",face="floor",facing="north")
d.set(0,3,0,"observer",facing="east")
d.set(2,3,0,"observer",facing="west")
for sx,px in ((-1,-2),(3,4)):
    d.set(sx,2,0,S); d.set(sx,3,0,"redstone_wire"); d.set(px,2,0,S); d.set(px,3,0,"redstone_wire")
d.set(-1,-1,0,"observer",facing="up")
d.set(-1,-2,0,"note_block")
d.set(0,-2,0,"observer",facing="west")
d.save("d2.json")
