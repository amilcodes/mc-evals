from pdbuild import Design
from v1full import singles, sdist, CROSS
P=-2
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
    # bus
    d.set(-2,0,1,"stone"); d.set(-2,1,1,"redstone_wire",**CROSS)
    d.set(-2,-1,1,"observer",facing="down")
    d.set(-2,2,1,"stone"); d.set(-2,3,1,"observer",facing="up")
    # bottom: M'' net, obs1, obs2, D2, Pt column
    dust(d,-2,P,1); dust(d,-3,P,1); dust(d,-3,P,0)
    d.set(-3,-1,0,"stone"); d.set(-2,-1,0,"observer",facing="east")
    d.set(-2,P,2,"observer",facing="south")
    rep(d,0,P,2,"north",1)
    for x in (0,-1,-2): dust(d,x,P,3)
    rep(d,-1,P,2,"south",1); rep(d,-1,P,1,"south",4)
    # top plane (y=4): monostable
    T=4
    dust(d,3,T,2); dust(d,3,T,3); dust(d,2,T,3,sup=None)
    for x,dl in ((2,4),(1,4),(0,4)): rep(d,x,T,2,"east",dl,sup=None)       # rear chain 24
    rep(d,1,T,3,"east",4,sup=None); rep(d,0,T,3,"east",2,sup=None)         # side chain 12
    dust(d,-1,T,3)
    d.set(-1,T,2,"comparator",facing="east",mode="subtract"); d.set(-1,T-1,2,"stone")
    rep(d,-2,T,2,"east",4)
    dust(d,-3,T,2); dust(d,-3,T,1)
    d.set(-2,T,1,"repeater",facing="west",delay=1)      # sits on observer, watched from below
    d.set(-3,2,0,"stone"); d.set(-3,3,0,"redstone_wire")
    return d
if __name__=="__main__":
    build().save("v3.json")
