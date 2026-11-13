def machine():
    d = Design("open")
    for p in [(-1,0),(-1,1),(-1,2),(3,0),(3,1),(3,2),(0,3),(1,3),(2,3),(0,-1),(1,-1),(2,-1)]:
        d.set(p[0],p[1],0,"stone")
    d.set(-3,1,0,"sticky_piston",facing="east")
    d.set(-2,1,0,"sticky_piston",facing="east")
    d.set(-1,-1,0,"sticky_piston",facing="up")
    # B feed: stones above row, dust on them, input via z
    d.set(-2,2,0,"stone"); d.set(-1,2,0,"stone")   # (-1,2) already stone
    d.set(-2,3,0,"redstone_wire"); d.set(-1,3,0,"redstone_wire")
    # A feed
    d.set(-2,-1,0,"stone"); d.set(-2,0,0,"redstone_wire")
    return d
