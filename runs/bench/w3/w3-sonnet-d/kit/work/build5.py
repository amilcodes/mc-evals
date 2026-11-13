from pdbuild import Design
exec(open('work/build.py').read())
def wall(x,y,z):
    return z!=0 and ((x in (-1,3) and 0<=y<=2) or (y in (-1,3) and 0<=x<=2))
def make5(delay=4):
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
    # chain along z=5, y=1: L0 (-3), R1..R4 at -4..-7, N4 dust -8, R5,R6 at -9,-10, N6 dust -11
    for x in (-4,-5,-6,-7,-9,-10): rep(x,1,5,"east",delay)
    dust(-8,1,5); dust(-11,1,5)
    obs(-4,1,4,"south"); obs(-6,1,4,"south")
    # P_Q row z=3
    for x in range(-9,-3): dust(x,1,3)
    for x in range(-5,-1): dust(x,1,2)
    rep(-2,1,1,"south",1)
    for z in (1,0,-1): dust(-5,1,z)
    for x in (-4,-3): dust(x,1,-1)
    rep(-2,1,-1,"west",1)
    # F branch: observer above R2 (-5,1,5)
    dust(-5,3,5); d.set(-5,2,5,"observer",facing="down"); dust(-5,4,4); dust(-5,5,3); dust(-5,5,2); dust(-5,5,1); dust(-5,5,0)
    for x in range(-4,0): dust(x,5,0)
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
    S(-4,2,0); d.set(-4,3,0,"redstone_wire")
    d.set(-3,2,0,"observer",facing="north"); d.set(-3,3,0,"redstone_wire")
    obs(-4,1,0,'east')
    return d
