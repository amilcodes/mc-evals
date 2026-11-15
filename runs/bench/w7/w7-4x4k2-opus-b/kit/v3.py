import v1, v2
from v1 import dust, rep, obs
from pdbuild import Design
def left():
    d=v2.left()
    # remove old chain beyond x<=-3 at y=-4/-5 (z any) except climb support (-5,-4,-3) and hops
    keep={(-5,-4,-3),(-3,-4,1),(-3,-4,2)}
    for p in list(d.blocks):
        x,y,z=p
        if y in (-4,-5) and x<=-3 and p not in keep: d.remove(*p)
    # Q column at x=-7 remains (y>=-3). rebuild chain
    rep(d,-3,-4,0,"east",1); rep(d,-4,-4,0,"east",4); rep(d,-5,-4,0,"east",3); dust(d,-6,-4,0)
    rep(d,-7,-4,0,"east",1)
    # OR_a
    rep(d,-6,-4,-1,"south",2); dust(d,-6,-4,-2); dust(d,-6,-4,-3)
    d.set(-5,-4,-3,"stone")
    # late
    rep(d,-1,-4,-1,"south",4); rep(d,-1,-4,-2,"south",4); dust(d,-1,-4,-3)
    rep(d,-2,-4,-3,"east",4); dust(d,-3,-4,-3)
    rep(d,-3,-4,-2,"north",4); dust(d,-3,-4,-1)
    rep(d,-4,-4,-1,"east",4); dust(d,-5,-4,-1)
    rep(d,-5,-4,-2,"south",4)
    return d
