exec(open("build3.py").read().split("def lefthalf")[0])
exec("def check"+open("build3.py").read().split("def check")[1])
def half():
    """symmetric part (mirrored)"""
    d=Design(); NET.clear()
    for y in (1,2):
        d.set(-3,y,0,SP,facing="east"); d.set(-2,y,0,SP,facing="east"); d.set(-1,y,0,"stone")
    for y in (0,3):
        d.set(-2,y,0,SP,facing="east"); d.set(-1,y,0,"stone")
    d.set(1,-2,0,SP,facing="up"); d.set(1,-1,0,"stone")
    d.set(1,5,0,SP,facing="down"); d.set(1,4,0,"stone")
    d.set(0,-3,0,SP,facing="up"); d.set(0,-2,0,SP,facing="up"); d.set(0,-1,0,"stone")
    d.set(0,6,0,SP,facing="down"); d.set(0,5,0,SP,facing="down"); d.set(0,4,0,"stone")
    # row gadget
    d.set(-2,2,1,"stone"); d.set(-2,3,1,"redstone_wire"); NET[(-2,3,1)]="Pr"
    d.set(-3,2,1,"observer",facing="north"); d.set(-3,3,1,"redstone_wire"); NET[(-3,3,1)]="Pr"
    W(d,-4,2,1,"Pr","stone"); W(d,-3,1,1,"Pr"); W(d,-2,1,1,"Pr")
    W(d,-3,2,2,"Pr","stone")
    d.set(-4,2,0,"observer",facing="north")
    R(d,-3,2,-1,"north",4); W(d,-3,2,-2,"Xr")
    zig(d,-4,-1,[2,1,0,-1,-2,-3,-4],"Xr",-2,"z")
    # S
    W(d,-2,0,-1,"S"); W(d,-2,-1,-2,"S")
    W(d,-2,4,-1,"S"); W(d,-2,4,-2,"S")
    for x in (-1,0): W(d,x,-2,-2,"S")
    W(d,-1,5,-2,"S","stone"); R(d,0,5,-2,"west",1,None); W(d,1,5,-2,"S",None); R(d,1,5,-1,"north",1,None)
    R(d,1,-2,-1,"north",1,"stone"); W(d,1,-2,-2,"S")
    # col P feed, pins, row, zig, top link
    W(d,-1,-1,0,"Pc"); R(d,-2,-1,0,"west",1); W(d,-3,-1,0,"Pc"); W(d,-3,-2,1,"Pc")
    for z in (1,2,3): W(d,-2,-1,z,"Pc")
    d.set(-2,-2,1,"stone")
    d.set(-2,-2,3,"stone")
    for x in (-1,0,1): W(d,x,-2,3,"Pc")
    zig(d,-2,4,[0,1,2,3,4,5],"Pc",3,"z")
    R(d,-2,5,2,"south"); W(d,-2,5,1,"Pc"); W(d,-3,5,1,"Pc","stone"); W(d,-3,5,0,"Pc")
    d.set(-2,4,0,"glass"); d.set(-2,5,0,"repeater",facing="west"); W(d,-1,5,0,"Pc")
    # X row + A reps
    for x in (0,1): W(d,x,-3,2,"Xb"); d.set(x,-2,2,"stone")
    R(d,0,-3,1,"south",4)
    W(d,0,6,2,"At"); R(d,0,6,1,"south",4)
    return d
def full():
    L=half(); netL=dict(NET)
    Rt=L.mirrored_x(3)
    d=Design("open"); d.merge(L); d.merge(Rt)
    net=dict(netL)
    for (x,y,z),n in netL.items(): net[(3-x,y,z)]=n
    NET.clear(); NET.update(net)
    def rm(*ps):
        for p in ps: d.remove(*p); NET.pop(p,None)
    # ---- left-only: obs2, obs1, X' riser, feeder, top link
    d.set(-1,-3,0,"observer",facing="east"); d.set(-2,-3,0,"stone")
    W(d,-3,-3,0,"Pc")
    d.set(-1,-3,3,"observer",facing="down")
    zig(d,-4,3,[6,5,4,3,2,1,0,-1,-2,-3,-4],"Xc",4,"z")
    d.set(-4,-4,4,"stone")
    for x in (-3,-2,-1): W(d,x,-4,3,"Xc")
    R(d,0,-4,3,"west",4); W(d,1,-4,3,"Xb")
    W(d,-3,6,3,"Xc"); W(d,-3,6,4,"Xc"); d.set(-2,6,3,"stone")
    R(d,-2,6,4,"west",4); W(d,-1,6,4,"At")
    for z in (4,3): W(d,0,6,z,"At")
    W(d,1,6,2,"At"); W(d,2,6,2,"At")
    # ---- S top link direction (flow west) and back-right S riser
    d.set(0,5,-2,"repeater",facing="east",delay=1); d.set(3,5,-2,"repeater",facing="east",delay=1)
    zig(d,7,4,[5,4,3,2,1,0,-1,-2,-3,-4],"S2",3,"z")
    W(d,7,6,3,"S2"); W(d,7,6,2,"S2"); W(d,7,6,1,"S2"); R(d,7,6,0,"south",1); W(d,7,6,-1,"S"); W(d,7,6,-2,"S","stone"); W(d,6,5,-2,"S","stone")
    d.set(6,6,1,"stone")
    # ---- S row repeater + S path (right)
    W(d,3,-2,-2,"S"); W(d,4,-4,0,"S"); W(d,4,-3,-1,"S","stone"); W(d,4,-2,-2,"S","stone")
    d.set(5,-3,-1,"stone")
    # P_c row rep (flow east)
    rm((2,-2,3)); R(d,2,-2,3,"west",1)
    d.set(4,-3,2,"stone")
    # ---- generator y=-4
    Y=-4
    def g(x,z,netn):
        d.set(x,Y-1,z,"glass"); d.set(x,Y,z,"redstone_wire"); NET[(x,Y,z)]=netn
    def gr(x,z,facing,delay=1): d.set(x,Y-1,z,"glass"); d.set(x,Y,z,"repeater",facing=facing,delay=delay)
    for x in range(-2,6): g(x,-2,"XrS")
    g(-2,-1,"XrS"); g(5,-1,"XrS")
    gr(-3,-1,"east"); gr(6,-1,"west")
    d.set(-2,Y-1,0,"stone"); d.set(-2,Y,0,"lever",face="floor",facing="north")
    for x in (-1,0,1,2,3): gr(x,0,"west",4)
    # S dust (4,-4,0) placed above
    g(-2,1,"L"); gr(-3,1,"east",4); g(-4,1,"L8"); gr(-4,2,"north",1)
    gr(4,1,"north",1); g(4,2,"L42"); g(5,2,"L42"); g(4,3,"L42"); g(4,4,"L42"); g(3,4,"L42"); g(2,4,"L42")
    gr(1,4,"east",1); g(0,4,"L44")
    for x in (-1,-2,-3): gr(x,4,"east",1)
    gr(5,1,"south",4); gr(5,0,"south",4)
    g(6,2,"L42"); g(6,1,"L42"); g(7,1,"L42"); gr(7,2,"north",1)
    return d
