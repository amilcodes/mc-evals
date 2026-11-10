from pdbuild import Design
from v1full import singles, sdist, CROSS
P=-2; T=4
def rep(d,x,y,z,facing,delay=1,sup="stone"):
    d.set(x,y,z,"repeater",facing=facing,delay=delay)
    if sup and d.get(x,y-1,z) is None: d.set(x,y-1,z,sup)
def dust(d,x,y,z,sup="stone",**kw):
    d.set(x,y,z,"redstone_wire",**kw)
    if sup and d.get(x,y-1,z) is None: d.set(x,y-1,z,sup)
def build():
    d=Design("open")
    d.set(-3,1,0,"sticky_piston",facing="east"); d.set(-2,1,0,"sticky_piston",facing="east")
    d.set(-1,1,0,"stone"); d.set(-1,0,0,"stone"); d.set(-1,2,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="up"); d.set(-1,-2,0,"stone")
    singles(d); sdist(d)
    d.set(2,T,1,"repeater",facing="east",delay=2)          # side delay 4 (also T/TL feed)
    # bus
    d.set(-2,0,1,"stone"); d.set(-2,1,1,"redstone_wire",**CROSS)
    d.set(-2,-1,1,"observer",facing="down")                # OBS_a watches W
    d.set(-2,2,1,"stone"); d.set(-2,3,1,"observer",facing="up")
    # bottom: comparator diode, W net, Pt chain, Pt watcher
    d.set(-1,P,1,"comparator",facing="east",mode="subtract"); d.set(-1,P-1,1,"stone")
    dust(d,-1,P,2); d.set(-1,-1,2,"stone"); d.set(-1,-1,1,"observer",facing="north")
    dust(d,-2,P,1); dust(d,-3,P,1); dust(d,-3,P,0)
    rep(d,-2,P,0,"west",4)
    # top monostable (rows z=1,2)
    dust(d,3,T,2)
    rep(d,2,T,2,"east",4,sup=None); rep(d,1,T,2,"east",4,sup=None)
    d.set(0,T,2,"comparator",facing="east",mode="subtract")
    rep(d,-1,T,2,"east",4); rep(d,-2,T,2,"east",4)
    dust(d,-3,T,2); dust(d,-3,T,1)
    d.set(-2,T,1,"repeater",facing="west",delay=1)
    d.set(-3,2,0,"stone"); d.set(-3,3,0,"redstone_wire")
    return d
if __name__=="__main__":
    build().save("v4.json")
