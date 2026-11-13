KEYS = ["(1,-3,0)","(1,-2,0)","(1,-1,0) ","(3,-1,0)","(-1,-1,0)","(0,-1,0)","(1,-2,-1)"]
def show(dd, flips=2, keys=KEYS, width=130):
    t = trace(dd, flips=flips, limit=600)
    for line in t.split("\n"):
        if line.startswith("flip") or line.startswith("place") or any(k in line for k in keys):
            print(line[:width] if not line.startswith("flip") else line)
def v4(p1d=4, hd=1):
    d = base()
    d.set(1,4,1,"lever",face="floor",facing="north")
    for x in (0,2): d.set(x,4,1,"redstone_wire")
    for sx,cx in ((-2,-1),(4,3)):
        d.set(cx,3,1,"redstone_wire"); d.set(cx,3,2,"redstone_wire")
        d.set(sx,1,2,"stone"); d.set(sx,2,2,"redstone_wire")
        d.set(sx,1,1,"stone"); d.set(sx,2,1,"redstone_wire"); d.set(sx,3,1,"stone")
    d.set(-2,0,3,"stone"); d.set(-2,1,3,"redstone_wire")
    d.set(-2,-1,4,"stone"); d.set(-2,0,4,"redstone_wire")
    d.set(-2,-2,5,"stone"); d.set(-2,-1,5,"redstone_wire")   # X
    dust(d,-2,6); dust(d,-2,7); dust(d,-2,8)
    fl(d,-1,8,"observer",facing="west")
    for x in range(0,5): dust(d,x,8)
    for z in (7,6,5,4,3,2,1): dust(d,4,z)
    rep(d,-1,6,"west",4); rep(d,0,6,"west",4); rep(d,1,6,"west",4); dust(d,2,6)
    dust(d,0,5); rep(d,1,5,"east",2); dust(d,2,5)
    rep(d,-2,4,"south",1); dust(d,0,4); dust(d,1,4)
    dust(d,-2,3); fl(d,-1,3,"stone"); rep(d,0,3,"east",1); dust(d,1,3)
    dust(d,-2,2); rep(d,-1,2,"south",hd)
    rep(d,-2,1,"south",1); dust(d,-1,1); fl(d,0,1,"observer",facing="west"); rep(d,1,1,"west",1); dust(d,2,1); dust(d,3,1)
    d.set(3,-1,1,"stone")
    dust(d,-2,0); d.set(2,-3,0,"glass"); d.set(2,-2,0,"redstone_wire")
    dust(d,-2,-1); fl(d,-1,-1,"observer",facing="west"); rep(d,0,-1,"west",p1d); dust(d,1,-1)
    fl(d,2,-1,"observer",facing="west"); dust(d,3,-1); dust(d,4,-1)
    return d
d4 = v4(); d4.save("v4.json")
r = test(d4); print(r.text[:900])
if not r.valid: show(d4)
