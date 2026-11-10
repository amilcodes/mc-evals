from pdbuild import Design
d = Design("open")
d.set(-6,5,0,"stone"); d.set(-6,6,0,"lever",face="floor",facing="north")
d.set(-5,5,0,"stone"); d.set(-5,6,0,"redstone_wire")
d.set(-4,6,0,"observer",facing="west")
d.set(-3,6,0,"sticky_piston",facing="east")
d.set(-2,6,0,"stone")
d.save("t1.json")
