from pdbuild import Design
from v1full import singles, sdist, CROSS
P=-2  # plane level
def rep(d,x,y,z,facing,delay=1,sup="stone"):
    d.set(x,y,z,"repeater",facing=facing,delay=delay)
    if sup: d.set(x,y-1,z,sup)
def dust(d,x,y,z,sup="stone",**kw):
    d.set(x,y,z,"redstone_wire",**kw)
    if sup: d.set(x,y-1,z,sup)
def build(yhome=(-1,1,0)):
    d=Design("open")
    # mechanism
    d.set(-3,1,0,"sticky_piston",facing="east"); d.set(-2,1,0,"sticky_piston",facing="east")
    d.set(*yhome,"stone"); d.set(-1,0,0,"stone"); d.set(-1,2,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="up"); d.set(-1,-2,0,"stone")
    singles(d); sdist(d)
    d.set(4,-1,3,"stone")
    # bus
    d.set(-2,0,1,"stone"); d.set(-2,1,1,"redstone_wire",**CROSS)
    d.set(-2,-1,1,"observer",facing="down")      # OBS_a watches M'' (-2,P,1)
    d.set(-2,0,2,"observer",facing="south")      # OBS_b watches R2 (-2,0,3)
    # M'' net
    dust(d,-2,P,1); dust(d,-3,P,1); dust(d,-3,P,0)
    d.set(-3,-1,0,"stone"); d.set(-2,-1,0,"observer",facing="east")   # obs2 watches Pt
    d.set(-2,P,2,"observer",facing="south")      # obs1 watches D2 (-2,P,3)
    # D2 + Pt column
    rep(d,0,P,2,"north",1)
    for x in (0,-1,-2): dust(d,x,P,3)
    rep(d,-1,P,2,"south",1); rep(d,-1,P,1,"south",4)
    # comparator loop
    rep(d,1,P,3,"west",4); dust(d,2,P,3); rep(d,3,P,3,"west",4); dust(d,4,P,3); dust(d,4,P,4)
    rep(d,3,P,4,"east",2)
    d.set(2,P,4,"comparator",facing="east",mode="subtract"); d.set(2,P-1,4,"stone")
    dust(d,1,P,4); rep(d,0,P,4,"east",2); rep(d,-1,P,4,"east",1); rep(d,-2,P,4,"east",1)
    dust(d,-3,P,4)
    # ladder up to Lb + OBS_b branch
    d.set(-3,P,3,"glass"); d.set(-3,-1,3,"redstone_wire")
    d.set(-3,-1,4,"glass"); d.set(-3,0,4,"redstone_wire")
    d.set(-3,0,3,"glass"); d.set(-3,1,3,"redstone_wire")
    d.set(-3,0,2,"stone"); d.set(-3,1,2,"redstone_wire")
    d.set(-3,0,1,"stone"); d.set(-3,1,1,"repeater",facing="south",delay=1)
    dust(d,-2,0,4); rep(d,-2,0,3,"south",2)
    return d
if __name__=="__main__":
    build().save("v2.json")
