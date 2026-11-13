def planar2(dtop=4, p1d=4):
    d = planar(dtop, p1d)
    for p in [(4,2),(4,3),(5,3),(5,2),(5,1),(5,0),(5,-1),(3,3),(3,4)]: d.remove(p[0],p[1],0)
    S = lambda x,y,b="stone",**k: d.set(x,y,0,b,**k)
    S(3,4); S(3,5,"repeater",facing="west",delay=dtop); S(4,4); S(4,5,"redstone_wire")
    S(5,3,"sticky_piston",facing="down"); S(5,4,"redstone_wire"); S(5,2,"redstone_block")
    S(5,0,"sticky_piston",facing="down"); S(5,-1,"redstone_block")
    return d
dq = planar2(); dq.save("p2.json")
r = test(dq); print(r.text[:1300])
if not r.valid: show(dq, keys=KP+["(5,3,0)","(5,1,0)","(5,-2,0)","(3,5,0)","(4,-3,0)"], width=150)
else: print(robust(dq,(-3,4,0)))
