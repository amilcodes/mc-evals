from pdbuild import Design
def mech_left(d):
    for y in (1,2):
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(-3,y,0,"sticky_piston",facing="east")
    d.set(-1,4,0,"sticky_piston",facing="down"); d.set(-1,5,1-1-1+1-1+1-1,"air") if False else None
    d.set(-1,-1,0,"sticky_piston",facing="up")
    d.set(-1,-2,0,"obsidian"); d.set(-1,5,0,"air") if False else None
    for x in (0,1):
        d.set(x,5,0,"sticky_piston",facing="down")
        d.set(x,-2,0,"sticky_piston",facing="up")
    # P2 driver chain
    d.set(-2,3,0,"observer",facing="up")
    d.set(-2,4,0,"observer",facing="north")
    # z=-1
    d.set(-1,4,-1,"observer",facing="north")          # OT
    for x in (0,1): d.set(x,5,-1,"observer",facing="north")
    d.set(-1,-1,-1,"observer",facing="north")         # OU
    for x in (0,1): d.set(x,-2,-1,"observer",facing="north")
    d.set(-3,1,-1,"glass"); d.set(-3,2,-1,"repeater",facing="north",delay=4)   # R-
    d.set(-2,2,-1,"observer",facing="west")           # B2'
    d.set(-2,3,-1,"glass"); d.set(-2,4,-1,"redstone_wire")
    d.set(-3,3,-1,"glass"); d.set(-3,4,-1,"redstone_wire")
    d.set(-3,5,-1,"observer",facing="up")             # PH feeder
    # z=-2 S1 chain (S0 at top)
    for y in range(-2,6): d.set(-2,y,-2,"observer",facing="up")
    d.set(-1,4,-2,"observer",facing="west")           # T feed
    for x in (-1,0,1): d.set(x,5,-2,"observer",facing="west")
    d.set(-1,-1,-2,"observer",facing="west")          # U feed
    for x in (-1,0,1): d.set(x,-2,-2,"observer",facing="west")
    # Q chain
    for y in (3,4,5): d.set(-3,y,-2,"observer",facing="up")
    d.set(-3,2,-2,"stone")
    return d
