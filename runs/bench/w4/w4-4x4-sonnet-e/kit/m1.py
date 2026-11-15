def module():
    d=Design()
    d.set(1,-3,0,"sticky_piston",facing="up")
    d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(1,-1,0,"stone")
    d.set(0,-1,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="east")
    def tap(px,py,lx,ly,side):
        s=1 if side>0 else -1
        d.set(px,py,s,"observer",facing="south" if s>0 else "north")
        d.set(px,py-1,2*s,"stone"); d.set(px,py,2*s,"redstone_wire")
        d.set(lx,ly-1,2*s,"stone"); d.set(lx,ly,2*s,"lever",face="floor",facing="north")
    tap(1,-3,2,-3,1)
    tap(1,-2,2,-2,-1)
    tap(-1,-1,-2,-1,1)
    return d
d=module()
d.save('m1.json')
