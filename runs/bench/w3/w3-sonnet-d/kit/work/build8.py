from pdbuild import Design
exec(open('work/build.py').read())
def wall(x,y,z):
    return z!=0 and ((x in (-1,3) and 0<=y<=2) or (y in (-1,3) and 0<=x<=2))
def make8(delay=4):
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
    for x in (-4,-5,-7,-9,-10): rep(x,1,5,"east",delay)
    for x in (-6,-8,-11): dust(x,1,5)
    obs(-4,1,4,"south"); obs(-7,1,4,"south")
    for x in range(-9,-3): dust(x,1,3)
    for x in range(-5,-1): dust(x,1,2)
    rep(-2,1,1,"south",1)
    for z in (1,0): dust(-5,1,z)
    dust(-4,0,0); dust(-3,0,0); rep(-2,0,0,"west",1)
    # F branch from N2 (-6,1,5)
    dust(-6,2,4); dust(-6,3,3); dust(-6,4,2); dust(-6,5,1); dust(-6,5,0)
    for x in range(-5,0): dust(x,5,0)
    d.set(-1,4,0,"observer",facing="up")
    # W logic
    dust(-8,2,4); dust(-8,3,3); rep(-8,3,2,'south',1); dust(-8,3,1)
    dust(-11,2,4); dust(-11,3,3); dust(-11,3,2); dust(-11,3,1); dust(-10,3,1)
    d.set(-9,3,1,"stone")
    d.set(-9,3,0,"redstone_wall_torch",facing="north")
    dust(-8,3,0)
    d.set(-7,2,0,"redstone_wall_torch",facing="east",lit=False)
    dust(-6,2,0)
    S(-5,2,0); d.set(-5,3,0,"redstone_wire")
    rep(-4,3,0,"west",4)
    d.set(-3,2,0,"observer",facing="north"); d.set(-3,3,0,"redstone_wire")
    obs(-4,1,0,'east')
    return d
