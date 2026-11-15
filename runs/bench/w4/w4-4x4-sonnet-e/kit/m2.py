def mechS(d):
    d.set(1,-3,0,"sticky_piston",facing="up")   # P1
    d.set(1,-2,0,"sticky_piston",facing="up")   # P2
    d.set(1,-1,0,"stone")                        # S_a
    d.set(0,-1,0,"stone")                        # S_b parked
    d.set(-1,-1,0,"sticky_piston",facing="east") # V
def testfeed(d):
    # P1 line from west
    for x in (0,-1,-2): d.set(x,-4,0,"stone"); d.set(x,-3,0,"redstone_wire")
    d.set(-3,-3,0,"observer",facing="west")
    d.set(-4,-4,0,"stone"); d.set(-4,-3,0,"redstone_wire")
    d.set(-5,-4,0,"stone"); d.set(-5,-3,0,"lever",face="floor",facing="north")
    # P2h line from z-
    for z in (-1,-2,-3): d.set(1,-3,z,"stone"); d.set(1,-2,z,"redstone_wire")
    d.set(1,-2,-4,"observer",facing="north")
    d.set(1,-3,-5,"stone"); d.set(1,-2,-5,"redstone_wire")
    d.set(2,-3,-5,"stone"); d.set(2,-2,-5,"lever",face="floor",facing="north")
    # V line from tail
    for x in (-2,-3): d.set(x,-2,0,"stone"); d.set(x,-1,0,"redstone_wire")
    d.set(-4,-1,0,"observer",facing="west")
    d.set(-5,-2,0,"stone"); d.set(-5,-1,0,"redstone_wire")
    d.set(-6,-2,0,"stone"); d.set(-6,-1,0,"lever",face="floor",facing="north")
    # P2f: observer (1,-2,1) facing down watch (1,-3,1)
    d.set(1,-2,1,"observer",facing="down")
    d.set(1,-4,1,"stone"); d.set(1,-3,1,"redstone_wire")
    d.set(2,-4,1,"stone"); d.set(2,-3,1,"lever",face="floor",facing="north")
d=Design(); mechS(d); testfeed(d); d.save('m2.json')
