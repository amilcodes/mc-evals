SP="sticky_piston"
NET={}
def W(d,x,y,z,net,sup="glass"):
    if sup: d.set(x,y-1,z,sup)
    d.set(x,y,z,"redstone_wire"); NET[(x,y,z)]=net
def R(d,x,y,z,facing,delay=1,sup="glass"):
    if sup: d.set(x,y-1,z,sup)
    d.set(x,y,z,"repeater",facing=facing,delay=delay)
def zig(d,x,z,ys,net,alt,axis):
    """zigzag riser: for y in ys alternate between base (x,z) and alt coordinate along axis"""
    for i,y in enumerate(ys):
        a=(i%2==1)
        if axis=="x": W(d,alt if a else x,y,z,net)
        else: W(d,x,y,alt if a else z,net)
def lefthalf():
    d=Design(); NET.clear()
    # ---- mechanism z=0
    for y in (1,2):
        d.set(-3,y,0,SP,facing="east"); d.set(-2,y,0,SP,facing="east"); d.set(-1,y,0,"stone")
    for y in (0,3):
        d.set(-2,y,0,SP,facing="east"); d.set(-1,y,0,"stone")
    d.set(1,-2,0,SP,facing="up"); d.set(1,-1,0,"stone")
    d.set(1,5,0,SP,facing="down"); d.set(1,4,0,"stone")
    d.set(0,-3,0,SP,facing="up"); d.set(0,-2,0,SP,facing="up"); d.set(0,-1,0,"stone")
    d.set(0,6,0,SP,facing="down"); d.set(0,5,0,SP,facing="down"); d.set(0,4,0,"stone")
    # ---- P_r local (back)
    d.set(-2,2,1,"stone"); d.set(-2,3,1,"redstone_wire"); NET[(-2,3,1)]="Pr"
    d.set(-3,2,1,"glass"); d.set(-3,3,1,"redstone_wire"); NET[(-3,3,1)]="Pr"
    W(d,-4,2,1,"Pr","stone"); W(d,-3,1,1,"Pr"); W(d,-2,1,1,"Pr")
    # P_r riser z=1: (-5,1),(-6,0),...,(-5,-5), foot (-4,-6,1)
    zig(d,-5,1,[1,0,-1,-2,-3,-4,-5],"Pr",-6,"x")
    # ---- A_r (front)
    W(d,-3,2,-1,"Ar","stone"); W(d,-3,2,-2,"Ar")
    zig(d,-4,-2,[2,1,0,-1,-2,-3,-4,-5,-6],"Ar",-5,"x")
    # ---- S (front)
    R(d,-2,0,-1,"north"); W(d,-2,0,-2,"S")
    W(d,-2,4,-1,"S"); W(d,-2,4,-2,"S")
    zig(d,-2,-3,[4,3,2,1,0,-1,-2,-3,-4,-5,-6],"S",-4,"z")
    d.set(-2,-6,-4,"stone")   # cut / support
    W(d,-1,5,-2,"S","stone"); R(d,0,5,-2,"west",1,None); W(d,1,5,-2,"S",None); R(d,1,5,-1,"north",1,None)
    R(d,1,-2,-1,"north",1,"stone"); W(d,1,-2,-2,"S")
    zig(d,1,-3,[-2,-3,-4,-5,-6],"S",-4,"z")
    # ---- P_c
    W(d,-1,-1,0,"Pc"); W(d,-2,-1,0,"Pc","stone")
    for z in (1,2,3): W(d,-2,-1,z,"Pc")
    zig(d,-2,4,[5,4,3,2,1,0,-1,-2,-3,-4,-5,-6],"Pc",5,"z")
    W(d,-3,5,4,"Pc"); W(d,-3,5,3,"Pc"); R(d,-3,5,2,"south"); W(d,-3,5,1,"Pc"); W(d,-3,5,0,"Pc")
    d.set(-2,4,0,"glass"); d.set(-2,5,0,"repeater",facing="west"); W(d,-1,5,0,"Pc")
    d.set(-2,-5,3,"stone")  # cut A_c row vs P_c riser
    # ---- A_c
    R(d,0,-3,1,"south",4,"stone")
    zig(d,0,2,[-3,-4,-5,-6],"Ac",3,"z")
    d.set(0,-5,1,"stone")   # cut P_r trunk vs A_c riser
    for z in range(1,8): W(d,0,7,z,"Ac")
    R(d,-1,7,7,"west",2); 
    zig(d,-2,7,[7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6],"Ac",-3,"x")
    for z in (4,5,7): W(d,-4,-6,z,"Ac")
    R(d,-4,-6,6,"north",2)
    return d
def full():
    L=lefthalf(); netL=dict(NET)
    Rt=L.mirrored_x(3)
    d=Design("open"); d.merge(L); d.merge(Rt)
    net=dict(netL)
    for (x,y,z),n in netL.items(): net[(3-x,y,z)]=n
    NET.clear(); NET.update(net)
    # ---- trunks
    # S z=-3 y=-6 x=-2..5 (feet at -2,1,2,5 exist)
    for x in range(-2,6):
        if x==0: R(d,x,-6,-3,"east")
        else: W(d,x,-6,-3,"S")
    def dip(z,net,xs,reps):
        for x in xs:
            if x in reps: R(d,x,-6,z,reps[x][0],reps[x][1])
            elif x in (1,2): W(d,x,-7,z,net,"stone")
            else: W(d,x,-6,z,net)
    dip(-1,"Ar",range(-4,8),{-2:("east",4),5:("west",4)})
    dip(1,"Pr",range(-4,8),{-3:("east",1),6:("west",1)})
    dip(3,"Ac",range(-4,8),{})
    dip(5,"Pc",range(-2,6),{-1:("east",1),4:("west",1)})
    # ---- generator y=-8
    Y=-8
    def g(x,z,net,sup="glass",**props):
        d.set(x,Y-1,z,sup); d.set(x,Y,z,"redstone_wire",**props); NET[(x,Y,z)]=net
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
    # L
    d.set(-5,Y-1,-4,"stone"); d.set(-5,Y,-4,"lever",face="floor",facing="north")
    for (x,z) in [(-4,-4),(-4,-3),(-3,-3),(-2,-3),(-1,-3),(-5,-3),(-6,-3),(-6,-2),(-6,-1),(-4,-5)]+[(x,-5) for x in range(-3,5)]:
        g(x,z,"L")
    gr(-1,-2,"north")
    gr(-6,0,"north",4); gr(-6,1,"north",4)
    g(-6,2,"L16"); 
    for x in range(-6,-1): g(x,3,"L16")
    gr(-4,2,"south",4); gr(-4,1,"south",4)
    g(-4,0,"L32"); g(-4,-1,"L32"); g(-3,-1,"L32"); gr(-2,-1,"west")
    # S late
    g(5,5,"Qc"); gr(6,5,"west",4)
    for z in range(-3,6): g(7,z,"SL")
    gr(7,-4,"south",4)
    # S logic
    d.set(5,Y,-5,"stone"); d.set(5,Y+1,-5,"redstone_torch",lit="true")   # T1
    d.set(7,Y,-5,"stone"); d.set(7,Y+1,-5,"redstone_torch",lit="true")   # T2
    d.set(6,Y,-5,"glass"); d.set(6,Y+1,-5,"redstone_wire",power=15); NET[(6,Y+1,-5)]="W"
    d.set(6,Y,-4,"glass"); d.set(6,Y+1,-4,"redstone_wire",power=14); NET[(6,Y+1,-4)]="W"
    d.set(6,Y+1,-3,"stone"); d.set(6,Y+2,-3,"redstone_torch",lit="false")  # T3
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
                        if not ab or ab[0] in ("glass","redstone_wire","repeater","redstone_torch"): bad.append(((x,y,z),n,p,NET[p],"step"))
    return bad
