from pdbuild import Design
exec(open('work/build.py').read().split("def make")[0])
def wall(x,y,z):
    return z!=0 and ((x in (-1,3) and 0<=y<=2) or (y in (-1,3) and 0<=x<=2))
def make2(delay=3):
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
    for k in range(1,7):
        rep(-2-2*k,1,5,"east",delay)
        dust(-3-2*k,1,5)
    obs(-5,1,4,"south"); obs(-9,1,4,"south")
    # P_Q line row z=3 then z=2
    for x in range(-23,-4): dust(x,1,3)
    for x in range(-5,-1): dust(x,1,2)
    rep(-2,1,1,"south",1)
    # P_Q2 branch to z=-1 side
    for z in (1,0,-1): dust(-4,1,z)
    dust(-3,1,-1); rep(-2,1,-1,"west",1)
    # F branch (y=5 route)
    dust(-7,2,4); dust(-7,3,3); dust(-7,4,2); dust(-7,5,1); dust(-7,5,0)
    for x in range(-6,0): dust(x,5,0)
    d.set(-1,4,0,"observer",facing="up")
    return d
