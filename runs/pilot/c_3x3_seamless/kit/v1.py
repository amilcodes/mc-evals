from pdbuild import Design
def rep(d,x,y,z,facing,delay=1,powered=False,sup=True):
    d.set(x,y,z,"repeater",facing=facing,delay=delay,powered=powered)
    if sup: d.set(x,y-1,z,"stone")
def dust(d,x,y,z,sup=True,**kw):
    d.set(x,y,z,"redstone_wire",**kw)
    if sup: d.set(x,y-1,z,"stone")
def mech(d):
    d.set(-3,1,0,"sticky_piston",facing="east")
    d.set(-2,1,0,"sticky_piston",facing="east")
    d.set(-1,1,0,"stone"); d.set(-1,0,0,"stone"); d.set(-1,2,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="up")
    d.set(-3,0,0,"stone")
def logic(d):
    # bus
    d.set(-2,0,1,"stone"); dust(d,-2,1,1,sup=False,north="side",south="side",east="side",west="side")
    rep(d,-2,0,2,"south"); dust(d,-2,0,3)
    # Pt column
    rep(d,-1,-1,1,"south",1); rep(d,-1,-1,2,"south",4); rep(d,-1,-1,3,"south",2)
    dust(d,-1,-1,4); dust(d,-1,-1,5)
    d.set(-1,-2,6,"stone"); d.set(-1,-1,6,"lever",face="floor",facing="north")
    # L line + obs1
    dust(d,-2,-1,5); dust(d,-3,-1,5)
    d.set(-2,-1,4,"observer",facing="south")
    rep(d,-4,-1,5,"east",4); rep(d,-5,-1,5,"east",4); rep(d,-6,-1,5,"east",2)
    dust(d,-7,-1,5)
    d.set(-7,-1,4,"observer",facing="south")
    for x in range(-7,-2): dust(d,x,-1,3)
    rep(d,-8,-1,5,"east",4); dust(d,-9,-1,5); dust(d,-10,-1,5)
    for z in (4,3,2,1): dust(d,-10,-1,z)
    dust(d,-10,0,0); dust(d,-9,0,0); rep(d,-8,0,0,"west",1)
    # monostable
    d.set(-7,0,0,"stone"); d.set(-6,0,0,"redstone_wall_torch",facing="east")
    d.set(-5,0,0,"comparator",facing="west",mode="subtract"); d.set(-5,-1,0,"stone")
    dust(d,-4,0,0)
    dust(d,-6,0,1); rep(d,-7,0,1,"east",4,True); dust(d,-8,0,1); dust(d,-8,0,2)
    rep(d,-7,0,2,"west",4,True); rep(d,-6,0,2,"west",1,True); dust(d,-5,0,2); rep(d,-5,0,1,"south",1,True)
    d.set(-5,0,3,"stone")
    # obs3
    d.set(-4,0,1,"observer",facing="north"); rep(d,-4,0,2,"north",2); d.set(-4,0,3,"stone")
if __name__=="__main__":
    d=Design("open"); mech(d); logic(d); d.save("v1m.json")
