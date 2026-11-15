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
XRF=-4   # lowest y of X_r riser (foot)
XCF=-4
def lefthalf(xrf=-4,xcf=-4):
    d=Design(); NET.clear()
    for y in (1,2):
        d.set(-3,y,0,SP,facing="east"); d.set(-2,y,0,SP,facing="east"); d.set(-1,y,0,"stone")
    for y in (0,3):
        d.set(-2,y,0,SP,facing="east"); d.set(-1,y,0,"stone")
    d.set(1,-2,0,SP,facing="up"); d.set(1,-1,0,"stone")
    d.set(1,5,0,SP,facing="down"); d.set(1,4,0,"stone")
    d.set(0,-3,0,SP,facing="up"); d.set(0,-2,0,SP,facing="up"); d.set(0,-1,0,"stone")
    d.set(0,6,0,SP,facing="down"); d.set(0,5,0,SP,facing="down"); d.set(0,4,0,"stone")
    # ---- row gadget
    d.set(-2,2,1,"stone"); d.set(-2,3,1,"redstone_wire"); NET[(-2,3,1)]="Pr"
    d.set(-3,2,1,"observer",facing="north"); d.set(-3,3,1,"redstone_wire"); NET[(-3,3,1)]="Pr"
    W(d,-4,2,1,"Pr","stone"); W(d,-3,1,1,"Pr"); W(d,-2,1,1,"Pr")
    W(d,-3,2,2,"Pr","stone")
    W(d,-4,2,0,"Pr")
    d.set(-4,2,-1,"observer",facing="north")
    R(d,-3,2,-1,"north",4); W(d,-3,2,-2,"Xr")
    zig(d,-4,-2,list(range(2,xrf-1,-1)),"Xr",-3,"z")
    # ---- S
    R(d,-2,0,-1,"north"); W(d,-2,0,-2,"S")
    W(d,-2,4,-1,"S"); W(d,-2,4,-2,"S")
    zig(d,-2,-3,[4,3,2,1,0,-1],"S",-4,"z")
    W(d,-1,-2,-4,"S")
    for x in (-1,0,1): W(d,x,-2,-3,"S")
    W(d,-1,5,-2,"S","stone"); R(d,0,5,-2,"west",1,None); W(d,1,5,-2,"S",None); R(d,1,5,-1,"north",1,None)
    R(d,1,-2,-1,"north",1,"stone"); W(d,1,-2,-2,"S")
    # ---- col gadget
    W(d,-1,-1,0,"Pc"); W(d,-2,-1,0,"Pc")
    for z in (1,2,3): W(d,-2,-1,z,"Pc")
    d.set(-1,-3,0,"observer",facing="east"); W(d,-2,-3,0,"Pc"); W(d,-3,-2,0,"Pc")
    for x in (-1,0,1): W(d,x,-2,3,"Pc")
    d.set(-1,-3,3,"observer",facing="down")
    zig(d,-2,4,[0,1,2,3,4,5],"Pc",3,"z")
    R(d,-2,5,2,"south"); W(d,-2,5,1,"Pc"); W(d,-3,5,1,"Pc","stone"); W(d,-3,5,0,"Pc")
    d.set(-2,4,0,"glass"); d.set(-2,5,0,"repeater",facing="west"); W(d,-1,5,0,"Pc")
    # X' riser + feeder + X row
    zig(d,-4,3,list(range(6,xcf-1,-1)),"Xc",4,"z")
    for x in (-3,-2,-1): W(d,x,-4,3,"Xc")
    R(d,0,-4,3,"west",4); W(d,1,-4,3,"Xb")
    for x in (0,1): W(d,x,-3,2,"Xb"); d.set(x,-2,2,"stone")
    R(d,0,-3,1,"south",4)
    # top A
    W(d,-3,6,3,"Xc"); W(d,-3,6,4,"Xc"); d.set(-2,6,3,"stone")
    R(d,-2,6,4,"west",4); W(d,-1,6,4,"At")
    for z in (4,3,2): W(d,0,6,z,"At")
    R(d,0,6,1,"south",4)
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
                        if not ab or ab[0] in ("glass","redstone_wire","repeater","redstone_torch","observer","sticky_piston","redstone_wall_torch"): bad.append(((x,y,z),n,p,NET[p],"step"))
    return bad
