exec(open("core.py").read())
W = "redstone_wire"
def v3():
    d = core()
    d.set(2, -2, 2, "repeater", facing="east", delay=3, powered=True)
    # control-side module changes
    for p in ((7,2,0),(7,3,0),(7,3,1),(7,4,1)): d.remove(*p)
    d.set(6,1,1,"glass"); d.set(6,2,1,"repeater",facing="south",delay=4)
    d.set(6,2,2,"stone"); d.set(6,3,2,W)
    d.set(7,2,1,"glass"); d.set(7,3,1,"repeater",facing="south",delay=4)
    d.set(7,3,2,"stone"); d.set(7,4,2,W)
    d.set(6,4,2,"glass"); d.set(6,5,2,W)
    d.set(4,6,2,"repeater",facing="east",delay=4)
    # QL chain and raw-top (as v2)
    d.set(5,5,0,"glass"); d.set(5,6,0,W)
    d.set(6,5,0,"glass"); d.set(6,6,0,"repeater",facing="east",delay=4)
    d.set(7,5,0,"glass"); d.set(7,6,0,"repeater",facing="east",delay=1)
    d.set(8,5,0,"stone"); d.set(8,6,0,W)
    d.set(6,4,1,"glass"); d.set(6,5,1,"repeater",facing="east",delay=1)
    d.set(7,5,1,"stone"); d.set(7,6,1,W)
    # lever block and side dust
    d.set(8,5,1,"stone"); d.set(8,6,1,W)
    d.set(9,5,1,"lever",face="wall",facing="east")
    d.set(8,3,1,"stone"); d.set(8,4,1,W)
    # comparator chain at z=2
    d.set(8,3,2,"glass"); d.set(8,4,2,"comparator",facing="east",mode="subtract")
    d.set(9,3,2,"glass"); d.set(9,4,2,W,**CROSS)
    d.set(9,5,2,"observer",facing="up"); d.set(9,6,2,"repeater",facing="west",delay=4)
    d.set(8,5,2,"stone"); d.set(8,6,2,W)
    # spiral down
    d.set(8,2,0,"stone"); d.set(8,3,0,W)
    d.set(9,1,0,"stone"); d.set(9,2,0,W)
    d.set(9,0,1,"stone"); d.set(9,1,1,W)
    d.set(8,-1,1,"stone"); d.set(8,0,1,W)
    d.set(8,-2,2,"stone"); d.set(8,-1,2,W)
    d.set(7,-2,2,"redstone_wall_torch",facing="west",lit=True)
    for x in (5,6):
        d.set(x,-3,2,"stone"); d.set(x,-2,2,W,power=15)
    return d
