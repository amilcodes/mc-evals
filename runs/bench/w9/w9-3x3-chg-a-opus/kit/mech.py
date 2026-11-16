def mech():
    d = Design("open")
    # static frame
    for p in [(0,-1),(2,-1),(2,3)]: d.set(p[0],p[1],0,"stone")
    for y in range(3):
        d.set(-1,y,0,"stone"); d.set(3,y,0,"stone")
        d.set(0,y,0,"air") if False else None
    d.set(0,0,0,"stone"); d.set(0,1,0,"stone"); d.set(0,2,0,"stone")
    d.set(2,0,0,"stone"); d.set(2,1,0,"stone"); d.set(2,2,0,"stone")
    # middle column, open state
    d.set(0,3,0,"stone")   # E2
    d.set(1,3,0,"stone")   # C
    d.set(1,-1,0,"stone")  # E1
    d.set(1,4,0,"sticky_piston",facing="down")  # T
    d.set(-1,3,0,"sticky_piston",facing="east") # K
    d.set(1,-2,0,"sticky_piston",facing="up")   # B
    d.set(1,-3,0,"sticky_piston",facing="up")   # Q
    # levers
    d.set(2,4,0,"lever",face="floor",facing="north")   # T lever on (2,3)
    d.set(-2,2,0,"stone"); d.set(-2,3,0,"lever",face="floor",facing="north")  # K
    d.set(2,-3,0,"stone"); d.set(2,-2,0,"lever",face="floor",facing="north")  # B lever adjacent to B(1,-2)
    d.set(2,-5,0,"stone"); d.set(2,-4,0,"lever",face="floor",facing="north")  # Q? not adjacent
    return d
