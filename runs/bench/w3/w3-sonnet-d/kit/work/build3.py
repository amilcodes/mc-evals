from pdbuild import Design
exec(open('work/build.py').read())
def wall(x,y,z):
    return z!=0 and ((x in (-1,3) and 0<=y<=2) or (y in (-1,3) and 0<=x<=2))
def make3(delay=4):
    d=make()
    def S(x,y,z):
        if not wall(x,y,z): d.set(x,y,z,"stone")
    def dust(x,y,z):
        d.set(x,y,z,"redstone_wire"); S(x,y-1,z)
    def rep(x,y,z,facing,dl=delay):
        d.set(x,y,z,"repeater",facing=facing,delay=dl); S(x,y-1,z)
    def obs(x,y,z,facing): d.set(x,y,z,"observer",facing=facing)
    d.set(-2,1,0,"sticky_piston",facing="east")   # Q
    d.set(-3,1,0,"sticky_piston",facing="east")   # R
    d.set(-1,3,0,"sticky_piston",facing="down")   # F
    NK=9
    for k in range(1,NK+1):
        rep(-2-2*k,1,5,"east",delay)
        dust(-3-2*k,1,5)
    # Q pulse observers at N1,N3,N5,N7
    for k in (1,3,6,9): obs(-3-2*k,1,4,"south")
    # P_Q line
    for x in range(-21,-12): dust(x,1,3)
    rep(-12,1,3,"west",1)
    for x in range(-11,-4): dust(x,1,3)
    for x in range(-5,-1): dust(x,1,2)
    rep(-2,1,1,"south",1)
    for z in (1,0,-1): dust(-5,1,z)
    for x in (-4,-3): dust(x,1,-1)
    rep(-2,1,-1,"west",1)
    # F branch (y=5 route) from N2 (-7,1,5)
    dust(-7,2,4); dust(-7,3,3); dust(-7,4,2); dust(-7,5,1); dust(-7,5,0)
    for x in range(-6,0): dust(x,5,0)
    d.set(-1,4,0,"observer",facing="up")
    # W logic
    # N4 copy (-11,1,5) -> up
    dust(-11,2,4); dust(-11,3,3); rep(-11,3,2,'south',1); dust(-11,3,1)
    # N6 copy (-15,1,5)
    dust(-17,2,4); dust(-17,3,3); dust(-17,3,2); dust(-17,3,1)
    for x in (-16,-15,-14,-13): dust(x,3,1)
    d.set(-12,3,1,"stone")   # S6
    d.set(-12,3,0,"redstone_wall_torch",facing="north")  # torch1 on S6 (south of it)
    dust(-11,3,0)   # OR dust (support (-11,2,0) = B_or)
    d.set(-10,2,0,"redstone_wall_torch",facing="east",lit=False)   # torch2 on B_or (-11,2,0)
    dust(-9,2,0)
    S(-8,2,0); d.set(-8,3,0,"redstone_wire")
    for x in range(-7,-3): dust(x,3,0)
    d.set(-3,2,0,"observer",facing="north"); d.set(-3,3,0,"redstone_wire")
    d.set(-4,2,0,"stone")
    return d
