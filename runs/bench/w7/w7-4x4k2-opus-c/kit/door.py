from pdbuild import Design
def left_half(d):
    # lines rows 1,2
    for y in (1,2):
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(-3,y,0,"sticky_piston",facing="east")
        d.set(-3,y,1,"observer",facing="north")
        d.set(-2,y,1,"observer",facing="west")
    d.set(-1,4,0,"sticky_piston",facing="down")   # slider T
    d.set(-1,-1,0,"sticky_piston",facing="up")    # slider U
    for x in (0,1):
        d.set(x,5,0,"sticky_piston",facing="down")
        d.set(x,-2,0,"sticky_piston",facing="up")
    # P2 driver from above
    d.set(-2,3,0,"observer",facing="up")
    d.set(-2,4,0,"observer",facing="north")
    d.set(-2,4,-1,"observer",facing="up")
    d.set(-2,5,-1,"observer",facing="west")
    # Q2 driver
    d.set(-3,1,-1,"stone"); d.set(-3,2,-1,"repeater",facing="north",delay=4)
    # S1 vertical chain at x=-2,z=-2, source observer at (-2,2,-2) watching (-2,2,-3)
    d.set(-2,2,-2,"observer",facing="north")
    for y in (3,4,5): d.set(-2,y,-2,"observer",facing="down")
    for y in (1,0,-1,-2): d.set(-2,y,-2,"observer",facing="up")
    # top chain
    for x in (-1,0,1): d.set(x,5,-2,"observer",facing="west")
    d.set(-1,4,-2,"observer",facing="up")
    d.set(-1,4,-1,"observer",facing="north")
    for x in (0,1): d.set(x,5,-1,"observer",facing="north")
    # bottom chain
    for x in (-1,0,1): d.set(x,-2,-2,"observer",facing="west")
    d.set(-1,-1,-2,"observer",facing="down")
    d.set(-1,-1,-1,"observer",facing="north")
    for x in (0,1): d.set(x,-2,-1,"observer",facing="north")
    return d
