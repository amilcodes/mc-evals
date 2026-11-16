exec(open('work/build4.py').read())
M = 11; Y0 = -3
def branch5(d,zb,yt,xt,items,zend,zreps=(),first=1):
    rep(d,M-1,Y0,zb,"east",first)
    x=M-2; y=Y0
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
def feeds5(d):
    d.set(3,-1,-1,"repeater",facing="north",delay=1); d.set(3,-2,-1,"stone")
    d.set(-1,-1,0,"repeater",facing="west",delay=1); d.set(-1,-2,0,"stone")
    d.set(-2,-1,0,"observer",facing="west"); d.set(-3,-1,0,"redstone_wire"); d.set(-3,-2,0,"stone")
    d.set(0,-2,0,"observer",facing="down"); d.set(0,-3,0,"redstone_wire"); d.set(0,-4,0,"stone")
    d.set(1,-3,-1,"repeater",facing="north",delay=3); d.set(1,-4,-1,"stone")
    d.set(1,-3,-2,"observer",facing="north")
    d.set(2,-2,0,"stone"); d.set(2,-2,1,"redstone_wire"); d.set(2,-3,1,"stone")
    d.set(3,-2,0,"observer",facing="up"); d.set(3,-3,0,"stone")
    d.set(2,-3,0,"repeater",facing="east",delay=3); d.set(2,-4,0,"stone")
def logic5(d):
    for z in range(-6,9): wire(d,M,Y0,z)
    d.set(M+1,Y0-1,0,"lever",face="wall",facing="east")
    branch5(d,-2,-1,3,[('r',4),('r',4),('r',1)],-2)
    branch5(d,-4,-1,3,[('r',4),('r',4),('r',3)],-3)
    branch5(d,-6,-3,1,[('r',2)],-3)
    branch5(d,2,-2,2,[('r',4),('r',4),('r',3)],2)
    branch5(d,4,-2,2,[('r',4),('r',4),('r',4),('o',),('r',4)],3,first=4)
    branch5(d,6,-3,0,[('r',4),('r',2)],1)
    branch5(d,8,-2,-3,[('r',4),('r',4),('r',4),('r',2)],1,((4,1),))
def simple5(d):
    rep(d,M-1,Y0,0,"east",1)
    for p in [(9,-3,0),(8,-2,0),(7,-1,0),(6,0,0),(5,1,0),
              (6,1,1),(5,2,1),(4,3,1),(3,4,1),(-1,5,0),(-1,5,1),(-2,4,1),(-3,3,1),(-3,2,0),(-3,2,-1),(-2,1,-1)]:
        wire(d,*p)
    d.set(2,4,1,"repeater",facing="east",delay=1)
    d.set(1,4,1,"redstone_wire"); d.set(0,4,1,"redstone_wire")
    for x in range(3): d.set(x,5,0,"redstone_wire")
def full7():
    d=Design("open"); core(d); feeds5(d); logic5(d); simple5(d); return d
