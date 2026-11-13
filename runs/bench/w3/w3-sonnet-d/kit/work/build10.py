from pdbuild import Design
def wall(x,y,z):
    return z!=0 and ((x in (-1,3) and 0<=y<=2) or (y in (-1,3) and 0<=x<=2))
def make10(delay=4):
    d=Design("open")
    def S(x,y,z):
        if not wall(x,y,z): d.set(x,y,z,"stone")
    def dust(x,y,z):
        d.set(x,y,z,"redstone_wire"); S(x,y-1,z)
    def rep(x,y,z,facing,dl=delay):
        d.set(x,y,z,"repeater",facing=facing,delay=dl); S(x,y-1,z)
    def obs(x,y,z,facing): d.set(x,y,z,"observer",facing=facing)
    for p in [(-1,0),(-1,1),(-1,2),(0,3),(1,3),(2,3),(3,0),(3,1),(3,2),(0,-1),(1,-1),(2,-1)]:
        S(p[0],p[1],0)
    for x in (0,1,2):
        d.set(x,4,0,"sticky_piston",facing="down"); rep(x,4,1,"south",1)
        dust(x,4,2)
    for x in (0,1,2):
        d.set(x,-2,0,"sticky_piston",facing="up"); rep(x,-2,1,"south",1); dust(x,-2,2)
    # top bus west end (U3) and east branch to E1
    dust(-1,4,2)
    dust(3,4,2); dust(4,4,2); dust(4,4,1); dust(5,4,1); dust(5,3,2); dust(5,2,3); dust(5,1,4)
    dust(4,1,4); dust(4,1,3); dust(4,1,2)
    rep(4,1,1,"south",1); d.set(4,1,0,"sticky_piston",facing="west")
    # bottom bus west end
    dust(-1,-2,2); dust(-2,-2,2)
    # trunk: L0 (-3,1,4), O (-2,1,4)
    dust(-3,1,4); dust(-2,1,4)
    dust(-2,2,3); dust(-2,3,2)           # up-branch, then (-1,4,2)
    dust(-3,0,3); dust(-3,-1,2)          # down-branch, then (-2,-2,2)
    # lever hanging from stone above L0
    S(-3,3,4); d.set(-3,2,4,"lever",face="ceiling",facing="north")
    # Q, R, F
    d.set(-2,1,0,"sticky_piston",facing="east")
    d.set(-3,1,0,"sticky_piston",facing="east")
    d.set(-1,3,0,"sticky_piston",facing="down")
    # chain along z=4,y=1: L0 (-3), R1 -4, R2 -5, N2 -6, R3 -7, N3 -8, R4 -9, R5 -10, N5 -11
    for x in (-4,-5,-7,-9): rep(x,1,4,"east",delay)
    for x in (-6,-8,-10): dust(x,1,4)
    obs(-4,1,3,"south"); obs(-7,1,3,"south")
    for x in range(-7,-3): dust(x,1,2)
    rep(-3,1,2,'west',1); d.set(-3,0,2,'glass'); dust(-2,1,2)
    rep(-2,1,1,"south",1)
    for z in (1,0): dust(-5,1,z)
    dust(-4,0,0); dust(-3,0,0); rep(-2,0,0,"west",1)
    # F branch from N2 (-6,1,4)
    dust(-6,2,3); dust(-6,3,2); dust(-6,4,1); dust(-6,5,0)
    for x in range(-5,0): dust(x,5,0)
    d.set(-1,4,0,"observer",facing="up")
    # W logic
    dust(-8,2,3); dust(-8,3,2); rep(-8,3,1,'south',1)
    dust(-10,2,3); dust(-10,3,2); rep(-10,3,1,'south',4)
    d.set(-10,3,0,'stone')
    d.set(-9,3,0,"redstone_wall_torch",facing="east")
    dust(-8,3,0)
    d.set(-7,2,0,"redstone_wall_torch",facing="east",lit=False)
    dust(-6,2,0)
    S(-5,2,0); d.set(-5,3,0,"redstone_wire")
    rep(-4,3,0,"west",4)
    d.set(-3,2,0,"observer",facing="north"); d.set(-3,3,0,"redstone_wire")
    obs(-4,1,0,'east')
    return d
