M = 13
def core(d):
    S = "stone"
    for p in [(-1,0),(-1,1),(-1,2),(3,0),(3,1),(3,2),(0,3),(1,3),(2,3),(0,-1),(1,-1),(2,-1)]:
        d.set(p[0],p[1],0,S)
    d.set(-2,0,0,"sticky_piston",facing="east"); d.set(-2,1,0,"sticky_piston",facing="east")
    d.set(4,0,0,"sticky_piston",facing="west"); d.set(4,1,0,"sticky_piston",facing="west")
    for x in range(3): d.set(x,4,0,"sticky_piston",facing="down")
    d.set(1,-2,0,"sticky_piston",facing="up"); d.set(1,-3,0,"sticky_piston",facing="up")
    d.set(3,-1,0,"sticky_piston",facing="west")
def feeds(d):
    d.set(3,-1,-1,"repeater",facing="north",delay=1); d.set(3,-2,-1,"stone")       # R2
    d.set(-1,-1,0,"repeater",facing="west",delay=1); d.set(-1,-2,0,"stone")        # A-high pulse2
    d.set(-2,-1,0,"observer",facing="west"); d.set(-3,-1,0,"redstone_wire"); d.set(-3,-2,0,"stone")
    d.set(0,-2,0,"observer",facing="down"); d.set(0,-3,0,"redstone_wire"); d.set(0,-4,0,"stone")  # spit
    d.set(1,-4,0,"stone")                                                          # B
    d.set(1,-4,-1,"repeater",facing="north",delay=3); d.set(1,-5,-1,"stone")
    d.set(1,-4,-2,"observer",facing="north")
    d.set(2,-4,0,"repeater",facing="east",delay=3); d.set(2,-5,0,"stone")
    d.set(3,-4,0,"observer",facing="east"); d.set(4,-4,0,"redstone_wire"); d.set(4,-5,0,"stone")
    d.set(2,-2,0,"stone"); d.set(2,-2,-1,"redstone_wire"); d.set(2,-3,-1,"stone")  # A-low
def wire(d,x,y,z): d.set(x,y,z,"redstone_wire"); d.set(x,y-1,z,"stone")
def rep(d,x,y,z,f,dl): d.set(x,y,z,"repeater",facing=f,delay=dl); d.set(x,y-1,z,"stone")
def zline(d,x,y,z0,z1,reps=()):
    # dust along z from z0 (far, negative) to z1 inclusive, with repeaters at given z (facing north)
    for z in range(z0,z1+1):
        if z in dict(reps): rep(d,x,y,z,"north",dict(reps)[z])
        else: wire(d,x,y,z)
def branch(d,zb,yt,xt,items,zend,zreps=()):
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
    zline(d,xt,yt,zb,zend,zreps)
def logic(d, P):
    for z in range(-16,1): wire(d,M,-4,z)
    d.set(M+1,-5,-9,"lever",face="wall",facing="east")
    branch(d,-2,-4,4,P['B2'],-1)
    branch(d,-4,-1,3,P['R2a'],-2)       # ends at (3,-1,-4)? line -4..-2
    branch(d,-6,-1,3,P['R2b'],-5)
    branch(d,-8,-2,2,P['Ala'],-2)
    branch(d,-10,-2,2,P['Alb'],-9)
    branch(d,-12,-4,1,P['B1'],-3, P.get('B1z',()))
    branch(d,-14,-3,0,P['O1'],-1, P.get('O1z',()))
    branch(d,-16,-2,-3,P['O2'],-1, P.get('O2z',()))

P=dict(B1=[('r',1)],B1z=((-8,1),),O1=[('r',4),('r',1)],O1z=((-7,1),),B2=[('r',4),('r',4),('r',1)],
 R2a=[('r',4),('r',4),('r',1)],R2b=[('r',4),('r',4),('r',3)],Ala=[('r',4),('r',4),('r',3)],
 Alb=[('r',4),('r',4),('r',4),('r',3),('o',),('r',1)],O2=[('r',4),('r',4),('r',3)],O2z=((-12,1),))
def full():
    d=Design("open"); core(d); feeds(d); logic(d,P)
    for z in range(-12,-2): 
        if z!=-8: d.set(1,-3,z,"stone")
    return d
def simple(d):
    rep(d,M-1,-4,0,"east",1)
    for p in [(M-2,-4,0),(M-3,-3,0),(M-4,-2,0),(M-5,-1,0),(M-6,0,0),(M-7,1,0)]+[(x,1,0) for x in range(5,M-7)]+[
              (6,2,1),(5,3,1),(4,4,1),(3,5,1),(1,5,1),(-1,5,0),(-1,5,1),(-2,4,1),(-3,3,1),(-3,2,0),(-3,2,-1),(-2,1,-1)]:
        wire(d,*p)
    rep(d,2,5,1,"east",1)
    for x in range(3): d.set(x,5,0,"redstone_wire")
def full2():
    d=full(); simple(d); return d
