from pdbuild import Design
def build():
    d=Design("open")
    S="stone"
    # tower
    d.set(-3,-3,0,S); d.set(-4,-3,0,"lever",face="wall",facing="west")
    d.set(-3,-2,0,"redstone_torch",lit="true")
    d.set(-3,-1,0,S)
    d.set(-3,0,0,"redstone_torch",lit="false")
    d.set(-3,1,0,S)
    d.set(-3,2,0,"redstone_wire")
    d.set(-2,2,0,S); d.set(-2,3,0,"redstone_wire")
    d.set(-1,3,0,S); d.set(-1,4,0,"redstone_wire")
    for x in range(3):
        d.set(x,4,0,"sticky_piston",facing="down"); d.set(x,5,0,"redstone_wire"); d.set(x,3,0,S)
    d.set(3,4,0,S); d.set(3,5,0,"redstone_wire")
    d.set(4,3,0,"observer",facing="up"); d.set(4,4,0,"redstone_wire"); d.set(4,2,0,S)
    # sides
    for y in (0,1):
        d.set(-2,y,0,"sticky_piston",facing="east"); d.set(-1,y,0,S)
        d.set(4,y,0,"sticky_piston",facing="west"); d.set(3,y,0,S)
    d.set(-1,2,0,S); d.set(3,2,0,S); d.set(2,-1,0,S)
    # center
    d.set(0,-1,0,S); d.set(1,-1,0,S)
    d.set(-1,-1,0,"sticky_piston",facing="east")
    d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(1,-3,0,"sticky_piston",facing="up")
    # e1
    d.set(4,-1,0,"observer",facing="up")
    d.set(3,-1,0,"observer",facing="east")
    d.set(2,-3,0,"glass"); d.set(2,-2,0,"redstone_wire")
    # right observer tower and line
    d.set(4,-2,0,"observer",facing="up"); d.set(4,-3,0,"observer",facing="up")
    d.set(4,-5,0,S); d.set(4,-4,0,"redstone_wire")
    for x in range(-1,4):
        d.set(x,-6,0,S); d.set(x,-5,0,"redstone_wire")
    d.set(-1,-4,0,"observer",facing="down")
    d.set(-1,-3,0,"note_block")
    d.set(-1,-2,0,"observer",facing="down")
    d.set(0,-4,0,S); d.set(0,-3,0,"repeater",facing="west",delay="4")
    d.set(0,-2,0,"observer",facing="down")
    return d
d=build(); d.save("d1.json")
