from pdbuild import Design
def make():
    d=Design("open")
    def wall(x,y,z):
        return z!=0 and ((x in (-1,3) and 0<=y<=2) or (y in (-1,3) and 0<=x<=2))
    def S(x,y,z):
        if not wall(x,y,z): d.set(x,y,z,"stone")
    def dust(x,y,z,sup=True):
        d.set(x,y,z,"redstone_wire")
        if sup: S(x,y-1,z)
    def rep(x,y,z,facing,delay=1):
        d.set(x,y,z,"repeater",facing=facing,delay=delay); S(x,y-1,z)
    # frame stones
    for p in [(-1,0),(-1,1),(-1,2),(0,3),(1,3),(2,3),(3,0),(3,1),(3,2),(0,-1),(1,-1),(2,-1)]:
        S(p[0],p[1],0)
    # singles
    for x in (0,1,2):
        d.set(x,4,0,"sticky_piston",facing="down"); rep(x,4,1,"south"); 
        d.set(x,4,2,"redstone_wire")  # support wall
    d.set(0,-2,0,"sticky_piston",facing="up"); d.set(1,-2,0,"sticky_piston",facing="up"); d.set(2,-2,0,"sticky_piston",facing="up")
    for x in (0,1,2):
        rep(x,-2,1,"south"); dust(x,-2,2)
    # top bus extension west + east
    dust(-1,4,2); dust(-2,4,2)
    dust(3,4,2); dust(4,4,2); dust(5,4,2); dust(5,3,3); dust(5,2,4); dust(5,1,5); dust(4,1,5); dust(4,1,4); dust(4,1,3); dust(4,1,2)
    rep(4,1,1,"south"); d.set(4,1,0,"sticky_piston",facing="west")
    # trunk
    dust(-2,1,5); dust(-2,2,4); dust(-2,3,3)
    dust(-3,1,5); dust(-3,0,4); dust(-3,-1,3); dust(-3,-2,2)
    # bottom bus west
    dust(-2,-2,2); dust(-1,-2,2)
    d.set(-3,1,4,"lever",face="wall",facing="west")
    return d
