SP="sticky_piston"
NET={}
def W(d,x,y,z,net,sup="glass",**props):
    if sup: d.set(x,y-1,z,sup)
    d.set(x,y,z,"redstone_wire",**props); NET[(x,y,z)]=net
def R(d,x,y,z,facing,delay=1,sup="glass"):
    if sup: d.set(x,y-1,z,sup)
    d.set(x,y,z,"repeater",facing=facing,delay=delay)
def zig(d,x,z,ys,net,alt,axis):
    for i,y in enumerate(ys):
        a=(i%2==1)
        if axis=="x": W(d,alt if a else x,y,z,net)
        else: W(d,x,y,alt if a else z,net)
TY=-5   # trunk level
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
    # P_r local + riser (z=1)
    d.set(-2,2,1,"stone"); d.set(-2,3,1,"redstone_wire"); NET[(-2,3,1)]="Pr"
    d.set(-3,2,1,"glass"); d.set(-3,3,1,"redstone_wire"); NET[(-3,3,1)]="Pr"
    W(d,-4,2,1,"Pr"); W(d,-3,1,1,"Pr"); W(d,-2,1,1,"Pr")
    zig(d,-4,1,[0,-1,-2,-3,-4],"Pr",-5,"x")
    # A_r
    W(d,-3,2,-1,"Ar","stone"); W(d,-3,2,-2,"Ar")
    zig(d,-4,-2,[2,1,0,-1,-2,-3,-4,-5],"Ar",-5,"x")
    # S
    R(d,-2,0,-1,"north"); W(d,-2,0,-2,"S")
    W(d,-2,4,-1,"S"); W(d,-2,4,-2,"S")
    zig(d,-2,-3,[4,3,2,1,0,-1,-2,-3,-4],"S",-4,"z")
    W(d,-1,5,-2,"S","stone"); R(d,0,5,-2,"west",1,None); W(d,1,5,-2,"S",None); R(d,1,5,-1,"north",1,None)
    R(d,1,-2,-1,"north",1,"stone")
    zig(d,1,-2,[-2,-3,-4],"S",-3,"z")
    # P_c
    W(d,-1,-1,0,"Pc"); W(d,-2,-1,0,"Pc","stone")
    for z in (1,2,3): W(d,-2,-1,z,"Pc")
    zig(d,-2,4,[5,4,3,2,1,0,-1,-2,-3,-4],"Pc",5,"z")
    W(d,-2,5,3,"Pc"); R(d,-2,5,2,"south"); W(d,-2,5,1,"Pc"); W(d,-3,5,1,"Pc"); W(d,-3,5,0,"Pc")
    d.set(-2,4,0,"glass"); d.set(-2,5,0,"repeater",facing="west"); W(d,-1,5,0,"Pc")
    # A_c
    d.set(0,-4,0,"stone"); R(d,0,-4,1,"south",4); W(d,0,-4,2,"Ac")
    zig(d,-4,3,[-4,-3,-2,-1,0,1,2,3,4,5,6],"Ac",-5,"x")
    W(d,-3,7,3,"Ac"); R(d,-2,7,3,"west",2); W(d,-1,7,3,"Ac")
    for z in (3,2,1): W(d,0,7,z,"Ac")
    return d
def full():
    L=lefthalf(); netL=dict(NET)
    Rt=L.mirrored_x(3)
    d=Design("open"); d.merge(L); d.merge(Rt)
    net=dict(netL)
    for (x,y,z),n in netL.items(): net[(3-x,y,z)]=n
    NET.clear(); NET.update(net)
    def row(z,netn,xs,reps,dips=(1,2)):
        for x in xs:
            if x in reps: R(d,x,TY,z,reps[x][0],reps[x][1])
            elif x in dips:
                W(d,x,TY-1,z,netn,None)
                if x in (1,2): d.set(x,TY-2,z,"stone")
            else: W(d,x,TY,z,netn)
    row(-3,"S",range(-1,5),{0:("east",1)},dips=())
    row(-1,"Ar",range(-5,9),{-3:("east",4),6:("west",4)})
    row(1,"Pr",range(-3,7),{-2:("east",1),5:("west",1)},dips=(0,1,2,3))
    d.set(-1,TY-1,1,"stone"); d.set(4,TY-1,1,"stone")
    row(3,"Ac",range(-3,7),{-2:("east",2),5:("west",2)})
    row(5,"Pc",range(-1,5),{})
    Y=TY-2
    def g(x,z,netn,sup="glass",**props):
        d.set(x,Y-1,z,sup); d.set(x,Y,z,"redstone_wire",**props); NET[(x,Y,z)]=netn
    def gr(x,z,facing,delay=1): d.set(x,Y-1,z,"glass"); d.set(x,Y,z,"repeater",facing=facing,delay=delay)
    LINE=dict(north="side",south="side",east="none",west="none",power=0)
    for zr,(xn,qn) in ((-1,("Xr","Qr")),(3,("Xc","Qc"))):
        g(-1,zr,xn); g(-1,zr+1,xn); g(-1,zr+2,xn,**LINE)
        gr(0,zr,"west",4)
        d.set(0,Y-1,zr+2,"glass"); d.set(0,Y,zr+2,"observer",facing="west")
        gr(3,zr,"west",4); g(4,zr,qn); gr(4,zr+1,"north",4)
        if zr==-1: g(4,zr+2,qn,**LINE)
        else: g(4,zr+2,qn,north="side",south="none",east="side",west="none",power=0)
        d.set(3,Y-1,zr+2,"glass"); d.set(3,Y,zr+2,"observer",facing="east")
    # S logic east-front
    d.set(4,TY-1,-4,"stone"); d.set(4,TY,-4,"redstone_torch",lit="false")       # T3 on Bk
    W(d,5,TY-1,-4,"W","glass",power=14); W(d,6,TY-1,-4,"W","glass",power=15)
    d.set(6,Y,-3,"stone"); d.set(6,Y+1,-3,"redstone_torch",lit="true")          # T1 on lever block
    d.set(5,Y,-3,"lever",face="wall",facing="west")
    d.set(7,Y,-4,"stone"); d.set(7,Y+1,-4,"redstone_torch",lit="true")          # T2
    gr(7,-3,"south",4)
    # L row z=-3
    for x in range(-4,5): g(x,-3,"L")
    gr(-1,-2,"north")
    g(-5,-3,"L"); g(-5,-2,"L"); g(-5,-1,"L")
    gr(-5,0,"north",4); gr(-5,1,"north",4)
    g(-5,2,"L16")
    for x in range(-5,-1): g(x,3,"L16")
    gr(-4,2,"south",4); gr(-4,1,"south",4)
    g(-4,0,"L32"); g(-3,0,"L32"); g(-3,-1,"L32"); gr(-2,-1,"west")
    # S late
    g(5,5,"Qc"); gr(6,5,"west",4)
    for z in range(-2,6): g(7,z,"SL")
    return d
def check(d):
    bad=[]
    for (x,y,z),n in NET.items():
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
            for dy in (-1,0,1):
                p=(x+dx,y+dy,z+dz)
                if p in NET and NET[p]!=n and d.get(*p) and d.get(*p)[0]=="redstone_wire":
                    if dy==0: bad.append(((x,y,z),n,p,NET[p]))
                    else:
                        low=(x,y,z) if dy==1 else p
                        ab=d.get(low[0],low[1]+1,low[2])
                        if not ab or ab[0] in ("glass","redstone_wire","repeater","redstone_torch","observer"): bad.append(((x,y,z),n,p,NET[p],"step"))
    return bad
