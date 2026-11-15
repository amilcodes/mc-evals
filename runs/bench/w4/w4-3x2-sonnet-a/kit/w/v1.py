from pdbuild import Design
d=Design("open")
# frame stones
for x in range(3):
    d.set(x,-1,0,"stone"); d.set(x,2,0,"stone")
for y in range(2):
    d.set(-1,y,0,"stone"); d.set(3,y,0,"stone")
# pistons
for x in range(3):
    d.set(x,-2,0,"sticky_piston",facing="up")
    d.set(x,3,0,"sticky_piston",facing="down")
    d.set(x,-2,1,"observer",facing="south")
    d.set(x,3,1,"observer",facing="south")
    # bottom bus
    d.set(x,-3,2,"stone"); d.set(x,-2,2,"redstone_wire")
    d.set(x,3,2,"redstone_wire")
# lever for bottom bus
d.set(-1,-3,2,"stone"); d.set(-1,-2,2,"lever",face="floor",facing="north")
# chain from lever up along x=-2 at z=2
d.set(-2,-2,2,"observer",facing="east")
for y in range(-1,2):
    d.set(-2,y,2,"observer",facing="down")
d.set(-2,2,2,"redstone_wire")
d.set(-1,2,2,"redstone_wire")
d.save("w/v1.json")
