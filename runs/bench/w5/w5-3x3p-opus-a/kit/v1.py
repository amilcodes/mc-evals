def build():
    d=Design("open")
    S="stone"
    # frame (open state)
    for y in range(3):
        d.set(-1,y,0,S); d.set(3,y,0,S)
    for p in [(0,-1),(2,-1),(1,-1),(0,3),(1,3),(2,3)]:
        d.set(p[0],p[1],0,S)
    # side pistons
    for y in range(3):
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(4,y,0,"sticky_piston",facing="west")
    d.set(-1,3,0,"sticky_piston",facing="east")   # Q
    d.set(1,4,0,"sticky_piston",facing="down")    # S
    d.set(1,5,0,"sticky_piston",facing="down")    # A
    d.set(1,-2,0,"sticky_piston",facing="up")     # B
    # lever
    d.set(4,4,0,S); d.set(4,5,0,"lever",face="floor",facing="north")
    # right drop
    d.set(4,3,0,"redstone_wire")
    d.set(4,1,1,S); d.set(4,2,1,"redstone_wire")
    d.set(3,3,1,"redstone_wire")
    d.set(2,4,1,"redstone_wire")
    d.set(1,4,1,"repeater",facing="east",delay=1)
    d.set(0,4,1,"redstone_wire")
    d.set(-1,3,1,"redstone_wire")
    d.set(-2,1,1,S); d.set(-2,2,1,"redstone_wire")
    d.set(-2,3,0,"redstone_wire")
    # Q chain
    d.set(-1,4,1,"glass"); d.set(-1,5,1,"redstone_wire")
    d.set(-1,4,0,"observer",facing="up")
    d.set(-1,5,0,"repeater",facing="south",delay=1)
    # S driver
    d.set(3,3,0,"glass"); d.set(3,4,0,"redstone_wire")
    d.set(2,4,0,"observer",facing="east")
    d.set(2,5,0,"observer",facing="west")   # O_A
    d.set(3,5,0,S)
    # A window
    d.set(4,4,-1,"observer",facing="up")
    d.set(4,5,-1,"repeater",facing="south",delay=1)
    d.set(3,5,-1,"observer",facing="east")
    d.set(2,4,-1,S); d.set(2,5,-1,"repeater",facing="east",delay=4)
    d.set(1,5,-1,S)
    # B chain
    for y in range(3,-3,-1):
        d.set(4,y,-1,"observer",facing="up")
    d.set(3,-2,-1,"observer",facing="east")
    d.set(2,-2,-1,"observer",facing="east")
    d.set(1,-2,-1,S)
    return d
v1=build()
v1.save("v1.json")
