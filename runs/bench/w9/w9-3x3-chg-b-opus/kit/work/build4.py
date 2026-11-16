exec(open('work/build3.py').read())
M = 12
def branch3(d,zb,yt,xt,items,zend,zreps=(),first=1):
    rep(d,M-1,-4,zb,"east",first)
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
def logic4(d):
    for z in range(-6,9): wire(d,M,-4,z)
    d.set(M+1,-5,0,"lever",face="wall",facing="east")
    branch3(d,-2,-1,3,[('r',4),('r',4),('r',1)],-2)
    branch3(d,-4,-1,3,[('r',4),('r',4),('r',3)],-3)
    branch3(d,-6,-4,1,[('r',2)],-3)
    branch3(d,2,-2,2,[('r',4),('r',4),('r',3)],2)
    branch3(d,4,-2,2,[('r',4),('r',4),('r',4),('o',),('r',4)],3,first=4)
    branch3(d,6,-3,0,[('r',4),('r',2)],1)
    branch3(d,8,-2,-3,[('r',4),('r',4),('r',4),('r',2)],1,((4,1),))
def simple2(d):
    rep(d,M-1,-4,0,"east",1)
    for p in [(10,-4,0),(9,-3,0),(8,-2,0),(7,-1,0),(6,0,0),(5,1,0),
              (6,1,1),(5,2,1),(4,3,1),(3,4,1),(2,5,1),(0,5,1),(-1,5,0),(-1,5,1),(-2,4,1),(-3,3,1),(-3,2,0),(-3,2,-1),(-2,1,-1)]:
        wire(d,*p)
    rep(d,1,5,1,"east",1)
    for x in range(3): d.set(x,5,0,"redstone_wire")
def full5():
    d=Design("open"); core(d); feeds3(d); logic4(d); simple2(d); return d
def simple3(d):
    rep(d,M-1,-4,0,"east",1)
    for p in [(10,-4,0),(9,-3,0),(8,-2,0),(7,-1,0),(6,0,0),(5,1,0),
              (6,1,1),(5,2,1),(4,3,1),(3,4,1),(-1,5,0),(-1,5,1),(-2,4,1),(-3,3,1),(-3,2,0),(-3,2,-1),(-2,1,-1)]:
        wire(d,*p)
    d.set(2,4,1,"repeater",facing="east",delay=1)
    d.set(1,4,1,"redstone_wire"); d.set(0,4,1,"redstone_wire")
    for x in range(3): d.set(x,5,0,"redstone_wire")
def full6():
    d=Design("open"); core(d); feeds3(d); logic4(d); simple3(d); return d
