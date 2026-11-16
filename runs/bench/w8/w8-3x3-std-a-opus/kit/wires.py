def wires(d):
    W="redstone_wire"
    # --- M path from lever (1,-2,1) ceiling on wall (1,-1,1)
    d.set(1,-2,1,"lever",face="ceiling",facing="north")
    for (x,y,z),(sx,sy,sz),sup in [((2,-2,1),(2,-3,1),"stone"),((3,-2,1),(3,-3,1),"stone"),((4,-1,1),(4,-2,1),"stone"),
                               ((5,0,1),(5,-1,1),"stone"),((5,1,0),(5,0,0),"stone"),((5,2,1),(5,1,1),"glass"),
                               ((4,2,1),(4,1,1),"stone"),((3,4,0),(3,3,0),"stone"),((3,5,1),(3,4,1),"glass"),
                               ((2,5,1),(2,4,1),"stone"),((1,5,1),(1,4,1),"stone"),((0,5,1),(0,4,1),"stone")]:
        d.set(sx,sy,sz,sup); d.set(x,y,z,W)
    d.set(3,3,1,W)
    # --- left signal lines
    for x in (-4,-5):
        d.set(x,0,0,"stone"); d.set(x,1,0,"repeater",facing="west",delay=1)
    # Q1 z=1 y=1
    d.set(-2,0,1,"glass")
    for x in (-3,-4,-5): d.set(x,0,1,"stone")
    for x in (-2,-3,-4,-5): d.set(x,1,1,W)
    # Q2 z=-1 y=2
    d.set(-2,1,-1,"stone"); d.set(-3,1,-1,"glass"); d.set(-4,1,-1,"stone"); d.set(-5,1,-1,"stone")
    for x in (-2,-3,-4,-5): d.set(x,2,-1,W)
    # V z=-1 y=4
    for x in range(-5,0):
        d.set(x,3,-1,"stone"); d.set(x,4,-1,W)
    # P2: QC dust (-2,3,0) on glass, (-2,3,1) on stone, then glass-supported line west
    d.set(-2,2,0,"glass"); d.set(-2,3,0,W); d.set(-2,2,1,"stone"); d.set(-2,3,1,W)
    for x in (-3,-4,-5): d.set(x,2,1,"glass"); d.set(x,3,1,W)
    return d
