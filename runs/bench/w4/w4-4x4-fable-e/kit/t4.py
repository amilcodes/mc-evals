SP="sticky_piston"
def mk(variant):
    d=Design()
    d.set(0,6,0,SP,facing="down"); d.set(0,5,0,SP,facing="down"); d.set(0,4,0,"stone")
    d.set(1,5,0,SP,facing="down"); d.set(1,4,0,"stone")
    d.set(-1,4,0,"glass"); d.set(-1,5,0,"redstone_wire")
    d.set(-2,4,0,"glass"); d.set(-2,5,0,"repeater",facing="west")
    d.set(-3,4,0,"glass"); d.set(-3,5,0,"redstone_wire")
    d.set(-4,5,0,"observer",facing="west"); d.set(-5,4,0,"stone"); d.set(-5,5,0,"redstone_wire")
    d.set(-6,4,0,"stone"); d.set(-6,5,0,"lever",face="floor",facing="north")
    if variant=="rep":
        d.set(0,5,-1,"glass"); d.set(0,6,-1,"repeater",facing="north")
        d.set(0,5,-2,"stone"); d.set(0,6,-2,"lever",face="floor",facing="north")
    else:
        d.set(0,5,1,"glass"); d.set(0,6,1,"redstone_wire"); d.set(0,5,2,"stone"); d.set(0,6,2,"lever",face="floor",facing="north")
    return d
for v in ("rep","dust"):
    lab=Lab(mk(v),walls=True)
    P=(-6,5,0); A=(0,6,-2) if v=="rep" else (0,6,2)
    out=[]
    for f in [P,A,P,P,A,P,P,A,P]:
        lab.flip(*f); lab.rest(); out.append(lab.doorway())
    print(v,out, lab.entity)
