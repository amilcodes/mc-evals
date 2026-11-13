def planar5(dtop=4, p1d=4):
    d = planar4(dtop, p1d)
    S = lambda x,y,b="stone",**k: d.set(x,y,0,b,**k)
    for p in [(5,5),(5,4),(5,3),(5,1),(5,0),(5,-1),(4,5),(4,4),(3,5),(3,4),(2,5)]: d.remove(p[0],p[1],0)
    S(2,5,"repeater",facing="west",delay=dtop); S(3,5)
    S(3,3); S(3,4,"redstone_wire"); S(4,2); S(4,3,"redstone_wire")
    S(4,-1,"observer",facing="up")
    return d
dt = planar5(); dt.save("p5.json")
r = test(dt); print(r.text[:1200])
if not r.valid: show(dt, keys=KP+["(2,5,0)","(3,4,0)","(4,3,0)","(4,-1,0)","(4,-3,0)","(2,-1,0)"], width=150)
else: print(robust(dt,(-2,2,1)))
