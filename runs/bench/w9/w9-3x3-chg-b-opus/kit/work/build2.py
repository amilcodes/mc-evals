exec(open('work/build.py').read())
def zline2(d,x,y,z0,z1,reps=()):
    R=dict(reps)
    zs = range(z0,z1+1) if z0<=z1 else range(z0,z1-1,-1)
    f = "north" if z0<=z1 else "south"
    for z in zs:
        if z in R: rep(d,x,y,z,f,R[z])
        else: wire(d,x,y,z)
def branch2(d,zb,yt,xt,items,zend,zreps=()):
    rep(d,M-1,-4,zb,"east",1)
    x=M-2; y=-4
    wire(d,x,y,zb)
    while y<yt:
        x-=1; y+=1; wire(d,x,y,zb)
    x-=1
    for it in items:
        if it[0]=='r': rep(d,x,y,zb,"east",it[1])
        else: d.set(x,y,zb,"observer",facing="east")
        x-=1
    while x>xt:
        wire(d,x,y,zb); x-=1
    assert x==xt, (zb,x,xt)
    zline2(d,xt,yt,zb,zend,zreps)
def feeds2(d):
    d.set(3,-1,-1,"repeater",facing="north",delay=1); d.set(3,-2,-1,"stone")       # R2 (neg side)
    d.set(-1,-1,0,"repeater",facing="west",delay=1); d.set(-1,-2,0,"stone")
    d.set(-2,-1,0,"observer",facing="west"); d.set(-3,-1,0,"redstone_wire"); d.set(-3,-2,0,"stone")
    d.set(0,-2,0,"observer",facing="down"); d.set(0,-3,0,"redstone_wire"); d.set(0,-4,0,"stone")
    d.set(1,-4,0,"stone")
    d.set(1,-4,-1,"repeater",facing="north",delay=3); d.set(1,-5,-1,"stone")       # B1 neg side
    d.set(1,-4,-2,"observer",facing="north")
    d.set(2,-4,0,"repeater",facing="east",delay=3); d.set(2,-5,0,"stone")
    d.set(3,-4,0,"observer",facing="east"); d.set(4,-4,0,"redstone_wire"); d.set(4,-5,0,"stone")
    d.set(2,-2,0,"stone"); d.set(2,-2,1,"redstone_wire"); d.set(2,-3,1,"stone")    # A-low pos side
def logic2(d):
    for z in range(-8,9): wire(d,M,-4,z)
    d.set(M+1,-5,0,"lever",face="wall",facing="east")
    branch2(d,-2,-4,4,[('r',4),('r',4),('r',1)],-1)
    branch2(d,-4,-1,3,[('r',4),('r',4),('r',1)],-2)
    branch2(d,-6,-1,3,[('r',4),('r',4),('r',3)],-5)
    branch2(d,-8,-4,1,[('r',2)],-3)
    branch2(d,2,-2,2,[('r',4),('r',4),('r',3)],2)
    branch2(d,4,-2,2,[('r',4),('r',4),('r',4),('r',3),('o',),('r',1)],3)
    branch2(d,6,-3,0,[('r',4),('r',2)],1)
    branch2(d,8,-2,-3,[('r',4),('r',4),('r',3)],1,((4,1),))
def full3():
    d=Design("open"); core(d); feeds2(d); logic2(d); simple(d); return d
