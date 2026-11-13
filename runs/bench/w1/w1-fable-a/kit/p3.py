def planar3(dtop=4, p1d=4):
    d = planar2(dtop, p1d)
    S = lambda x,y,b="stone",**k: d.set(x,y,0,b,**k)
    for p in [(5,3),(5,4),(5,2)]: d.remove(p[0],p[1],0)
    S(5,5,"redstone_wire"); S(5,4,"sticky_piston",facing="down"); S(5,3,"redstone_block")
    S(5,1,"redstone_wire",north="side",south="side",east="side",west="side")
    return d
dr = planar3(); dr.save("p3.json")
r = test(dr); print(r.text[:1000])
if not r.valid: show(dr, keys=KP+["(5,4,0)","(5,1,0)","(5,2,0)","(5,-2,0)","(4,-3,0)"], width=150)
else: print(robust(dr,(-3,4,0)))
