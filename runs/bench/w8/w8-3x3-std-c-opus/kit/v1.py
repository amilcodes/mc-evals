def build(dk=2, dx=4, dline=(4,4,4)):
    d = Design("open")
    S = d.set
    # mechanics
    for p,f in [((0,4,0),"down"),((1,4,0),"down"),((4,2,0),"west"),((4,1,0),"west"),((4,0,0),"west"),
                ((1,-2,0),"up"),((0,-2,0),"up"),((-2,1,0),"east"),((-3,1,0),"east"),((-1,-1,0),"up")]:
        S(*p,"sticky_piston",facing=f)
    for p in [(0,3),(1,3),(2,3),(3,2),(3,1),(3,0),(0,-1),(1,-1),(2,-1),(-1,0),(-1,1),(-1,2)]:
        S(p[0],p[1],0,"stone")
    # S network
    S(0,4,-1,"repeater",facing="north"); S(1,4,-1,"repeater",facing="north")
    S(4,2,-1,"repeater",facing="north"); S(4,1,-1,"glass")
    S(4,0,-1,"repeater",facing="north"); S(4,-1,-1,"stone")
    S(1,-2,-1,"repeater",facing="north"); S(1,-3,-1,"stone")
    S(0,-2,-1,"repeater",facing="north"); S(0,-3,-1,"stone")
    for x in range(0,5): S(x,-2,-2,"redstone_wire"); S(x,-3,-2,"stone")
    S(5,-1,-2,"redstone_wire"); S(5,-2,-2,"stone")
    S(4,0,-2,"redstone_wire"); S(4,-1,-2,"glass")
    S(5,1,-2,"redstone_wire"); S(5,0,-2,"glass")
    S(4,2,-2,"redstone_wire"); S(4,1,-2,"glass")
    S(3,3,-2,"redstone_wire")
    for x in range(0,3): S(x,4,-2,"redstone_wire")
    S(-1,-2,-2,"stone")                                   # LB
    S(-1,-3,-2,"lever",face="ceiling",facing="north")     # lever
    # NL torch on LB
    S(-2,-2,-2,"redstone_wall_torch",facing="west")
    # K' driver
    S(-1,-2,0,"redstone_wall_torch",facing="east"); S(-2,-2,0,"stone")   # KT on KA
    S(-2,-2,-1,"repeater",facing="north",delay=4); S(-2,-3,-1,"stone")
    S(-3,-2,0,"repeater",facing="west",delay=dk); S(-3,-3,0,"stone")
    # X driver
    S(-2,0,0,"redstone_wall_torch",facing="south"); S(-2,0,-1,"stone")  # XT on XA
    S(-2,-1,-2,"stone")                                   # strongly powered by NL torch
    S(-2,0,-2,"redstone_wire",north="side",south="side",east="side",west="side")  # cross
    S(-3,0,-1,"repeater",facing="west",delay=dx); S(-3,-1,-1,"stone")
    # NL delay line z=-2, y=-2
    S(-3,-2,-2,"redstone_wire"); S(-3,-3,-2,"stone")
    for i,dl in enumerate(dline):
        x=-4-i; S(x,-2,-2,"repeater",facing="east",delay=dl); S(x,-3,-2,"stone")
    xe=-4-len(dline)
    S(xe,-2,-2,"redstone_wire"); S(xe,-3,-2,"stone")
    S(xe,-2,-1,"redstone_wire"); S(xe,-3,-1,"stone")
    for x in range(xe,-3): S(x,-2,0,"redstone_wire"); S(x,-3,0,"stone")
    # riser to D_X (-4,0,-1)
    S(xe+1,-1,-1,"redstone_wire"); S(xe+1,-2,-1,"glass")
    S(xe+2,0,-1,"redstone_wire"); S(xe+2,-1,-1,"glass")
    for x in range(xe+3,-3): S(x,0,-1,"redstone_wire"); S(x,-1,-1,"glass")
    return d
