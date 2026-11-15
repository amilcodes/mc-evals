exec(open("build3.py").read().split("def lefthalf")[0])
exec("def check"+open("build3.py").read().split("def check")[1])
def lefthalf():
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
    W(d,-4,2,0,"Pr")
    d.set(-4,2,-1,"observer",facing="north")
    R(d,-3,2,-1,"north",4); W(d,-3,2,-2,"Xr")
    zig(d,-4,-2,[2,1,0,-1,-2,-3,-4],"Xr",-3,"z")
    # S (row at y=-2)
    R(d,-2,0,-1,"north"); W(d,-2,0,-2,"S")
    W(d,-2,4,-1,"S"); W(d,-2,4,-2,"S")
    zig(d,-2,-3,[4,3,2,1,0,-1],"S",-4,"z")
    W(d,-1,-2,-4,"S")
    for x in (-1,0,1): W(d,x,-2,-3,"S")
    W(d,-1,5,-2,"S","stone"); R(d,0,5,-2,"west",1,None); W(d,1,5,-2,"S",None); R(d,1,5,-1,"north",1,None)
    R(d,1,-2,-1,"north",1,"stone"); W(d,1,-2,-2,"S")
    # col gadget
    W(d,-1,-1,0,"Pc"); W(d,-2,-1,0,"Pc")
    for z in (1,2,3): W(d,-2,-1,z,"Pc")
    d.set(-1,-3,0,"observer",facing="east"); W(d,-2,-3,0,"Pc"); W(d,-3,-2,0,"Pc")
    for x in (-1,0,1): W(d,x,-2,3,"Pc")
    d.set(-1,-3,3,"observer",facing="down")
    zig(d,-2,4,[0,1,2,3,4,5],"Pc",3,"z")
    R(d,-2,5,2,"south"); W(d,-2,5,1,"Pc"); W(d,-3,5,1,"Pc","stone"); W(d,-3,5,0,"Pc")
    d.set(-2,4,0,"glass"); d.set(-2,5,0,"repeater",facing="west"); W(d,-1,5,0,"Pc")
    zig(d,-4,3,[6,5,4,3,2,1,0,-1,-2,-3,-4],"Xc",4,"z")
    for x in (-3,-2,-1): W(d,x,-4,3,"Xc")
    R(d,0,-4,3,"west",4); W(d,1,-4,3,"Xb")
    for x in (0,1): W(d,x,-3,2,"Xb"); d.set(x,-2,2,"stone")
    R(d,0,-3,1,"south",4)
    W(d,-3,6,3,"Xc"); W(d,-3,6,4,"Xc"); d.set(-2,6,3,"stone")
    R(d,-2,6,4,"west",4); W(d,-1,6,4,"At")
    for z in (4,3,2): W(d,0,6,z,"At")
    R(d,0,6,1,"south",4)
    return d
GY=-5
def full():
    L=lefthalf(); netL=dict(NET)
    Rt=L.mirrored_x(3)
    d=Design("open"); d.merge(L); d.merge(Rt)
    net=dict(netL)
    for (x,y,z),n in netL.items(): net[(3-x,y,z)]=n
    NET.clear(); NET.update(net)
    def rm(*ps):
        for p in ps: d.remove(*p); NET.pop(p,None)
    # delete right obs2 path, right feeder
    rm((4,-3,0),(5,-3,0),(5,-4,0),(6,-2,0),(6,-3,0))
    rm((6,-4,3),(5,-4,3),(4,-4,3),(6,-5,3),(5,-5,3),(4,-5,3),(3,-4,3),(3,-5,3),(2,-4,3),(2,-5,3))
    d.set(4,-3,3,"glass")
    d.set(-2,-2,3,"stone"); d.set(5,-2,3,"stone")
    rm((2,-2,3)); R(d,2,-2,3,"west",1)
    # S row repeater + S path (right)
    rm((2,-2,-3)); R(d,2,-2,-3,"east",1)
    W(d,4,-4,0,"S"); W(d,4,-3,-1,"S","stone"); W(d,4,-2,-2,"S")
    # cut stones
    for p in [(-2,-4,2),(-1,-4,2),(1,-4,2),(-2,-4,4),(-1,-4,4),(1,-4,4)]: d.set(*p,"stone")
    Y=GY
    def g(x,z,netn):
        d.set(x,Y-1,z,"glass"); d.set(x,Y,z,"redstone_wire"); NET[(x,Y,z)]=netn
    def gr(x,z,facing,delay=1): d.set(x,Y-1,z,"glass"); d.set(x,Y,z,"repeater",facing=facing,delay=delay)
    # X_r line z=-1
    for x in range(-4,8):
        if x==-3: gr(x,-1,"east")
        elif x==6: gr(x,-1,"west")
        else: g(x,-1,"Xr" if x in (-4,7) else "XrS")
    NET[(-4,Y,-1)]="Xr"; NET[(7,Y,-1)]="Xr"
    # X' line z=4
    for x in range(-4,8):
        if x==-3: gr(x,4,"east")
        elif x==6: gr(x,4,"west")
        else: g(x,4,"Xc" if x in (-4,7) else "XcS")
    # lever, chain
    d.set(-2,Y-1,0,"stone"); d.set(-2,Y,0,"lever",face="floor",facing="north")
    gr(-2,1,"north",4)
    for x in (-2,-1,0,1,2): g(x,2,"L8")
    g(-1,1,"L8")
    for x in (0,1,2,3): gr(x,1,"west",4)
    g(4,1,"S")
    gr(2,3,"north",1)
    gr(4,2,"north",4); g(4,3,"XcS"); g(5,3,"XcS"); g(5,2,"XcS")
    gr(5,1,"south",4); gr(5,0,"south",4)
    return d
