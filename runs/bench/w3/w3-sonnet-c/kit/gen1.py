exec(open('ctl2.py').read())   # helpers dust/rep/comp/modR/modF with plane Y=3
def D3(d,x,y,z,blk="redstone_wire",sup="stone",**kw):
    d.set(x,y,z,blk,**kw)
    if blk in ("redstone_wire","repeater","comparator") and sup:
        d.set(x,y-1,z,sup)
def dst(d,x,y,z,sup="stone"): D3(d,x,y,z,"redstone_wire",sup)
def rp(d,x,y,z,facing,delay=1): D3(d,x,y,z,"repeater",facing=facing,delay=delay)

def build(extra_lever=True):
    d=Design("open")
    for p in [(-1,0),(-1,1),(-1,2),(3,0),(3,1),(3,2),(0,3),(1,3),(2,3),(0,-1),(1,-1),(2,-1)]:
        d.set(p[0],p[1],0,"stone")
    d.set(-3,1,0,"sticky_piston",facing="east")
    d.set(-2,1,0,"sticky_piston",facing="east")
    d.set(-1,-1,0,"sticky_piston",facing="up")
    # B feed
    dst(d,-1,3,0,sup=None)
    d.set(-2,1,1,"stone"); dst(d,-2,2,1,sup=None)
    # P feed (back)
    dst(d,-4,1,0); dst(d,-5,1,0)
    # A feed
    dst(d,-2,-1,0); dst(d,-3,-1,0)
    # observers
    d.set(-3,1,1,"observer",facing="north"); d.set(-1,-1,1,"observer",facing="north")
    # domino net
    dst(d,-3,1,2); dst(d,-5,1,2)
    dst(d,-1,-1,2); dst(d,-2,-1,2); dst(d,-3,-1,2)
    dst(d,-4,0,2); dst(d,-6,2,2); dst(d,-7,3,2); dst(d,-7,3,3)
    dst(d,-6,3,3)
    for x in (-5,-4,-3,-2): dst(d,x,3,3)
    # trunk B
    for z in range(0,7): dst(d,-4,3,z)
    return d
