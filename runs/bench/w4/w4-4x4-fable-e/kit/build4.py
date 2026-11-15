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
    W(d,-4,-5,-1,"Xr")
    # S
    R(d,-2,0,-1,"north"); W(d,-2,0,-2,"S")
    W(d,-2,4,-1,"S"); W(d,-2,4,-2,"S")
    zig(d,-2,-3,[4,3,2,1,0,-1,-2,-3,-4],"S",-4,"z")
    W(d,-1,5,-2,"S","stone"); R(d,0,5,-2,"west",1,None); W(d,1,5,-2,"S",None); R(d,1,5,-1,"north",1,None)
    R(d,1,-2,-1,"north",1,"stone")
    zig(d,1,-2,[-2,-3,-4],"S",-3,"z")
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
    W(d,-4,-5,4,"Xc")
    for x in (-3,-2,-1): W(d,x,-4,3,"Xc")
    d.set(-2,-4,4,"stone"); d.set(-1,-4,4,"stone")
    R(d,0,-4,3,"west",4); W(d,1,-4,3,"Xb")
    for x in (0,1): W(d,x,-3,2,"Xb"); d.set(x,-2,2,"stone")
    R(d,0,-3,1,"south",4)
    W(d,-3,6,3,"Xc"); W(d,-3,6,4,"Xc"); d.set(-2,6,3,"stone")
    R(d,-2,6,4,"west",4); W(d,-1,6,4,"At")
    for z in (4,3,2): W(d,0,6,z,"At")
    R(d,0,6,1,"south",4)
    return d
TY=-5
def full():
    L=lefthalf(); netL=dict(NET)
    Rt=L.mirrored_x(3)
    d=Design("open"); d.merge(L); d.merge(Rt)
    net=dict(netL)
    for (x,y,z),n in netL.items(): net[(3-x,y,z)]=n
    NET.clear(); NET.update(net)
    def row(z,netn,xs,reps,dips):
        for x in xs:
            if x in reps: R(d,x,TY,z,reps[x][0],reps[x][1])
            elif x in dips:
                W(d,x,TY-1,z,netn,"stone")
            else: W(d,x,TY,z,netn)
    row(-3,"S",range(-1,5),{3:("west",1)},(0,))
    row(-1,"Xr",range(-3,7),{-1:("east",1),4:("west",1)},(1,2))
    row(4,"Xc",range(-3,7),{-3:("east",1),6:("west",1)},(1,2))
    Y=TY-2
    def g(x,z,netn):
        d.set(x,Y-1,z,"glass"); d.set(x,Y,z,"redstone_wire"); NET[(x,Y,z)]=netn
    def gr(x,z,facing,delay=1): d.set(x,Y-1,z,"glass"); d.set(x,Y,z,"repeater",facing=facing,delay=delay)
    # lever + X_r in A
    d.set(-1,Y-1,-1,"stone"); d.set(-1,Y,-1,"lever",face="floor",facing="north")
    gr(0,-1,"west",1)
    # L8
    gr(-1,0,"north",4)
    for z in (1,2,3,4): g(-1,z,"L8")
    gr(0,4,"west",1)
    # chain to L40 -> S block
    gr(-2,1,"east",4); g(-3,1,"c1"); gr(-3,0,"south",4); gr(-3,-1,"south",4)
    g(-3,-2,"c3"); g(-3,-3,"c3"); g(-2,-3,"c3"); gr(-1,-3,"west",4)
    # L42 east
    for x in range(1,7): g(x,-3,"L42")
    gr(6,-2,"north",3)
    for z in range(-1,5): g(6,z,"L48")
    g(5,4,"L48"); g(4,4,"L48"); gr(3,4,"east",1)
    gr(5,-1,"east",4); g(4,-1,"L56"); gr(3,-1,"east",4)
    return d
