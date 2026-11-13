def planar4(dtop=4, p1d=4):
    d = planar3(dtop, p1d)
    S = lambda x,y,b="stone",**k: d.set(x,y,0,b,**k)
    for p in [(-3,3),(-3,4),(-3,2),(-3,1),(-2,4),(-2,3),(0,4)]: d.remove(p[0],p[1],0)
    S(-2,2); S(-2,3,"redstone_wire")
    d.set(-2,2,1,"lever",face="wall",facing="south")
    S(0,4,"sticky_piston",facing="down"); S(0,5,"redstone_wire")
    return d
ds = planar4(); ds.save("p4.json")
r = test(ds); print(r.text[:1000])
if not r.valid: show(ds, keys=KP+["(-2,1,0)","(-2,0,0)","(0,4,0)","(0,5,0)","(-2,3,0)"], width=150)
else: print(robust(ds,(-2,2,1)))
