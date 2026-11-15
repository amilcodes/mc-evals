def build3(arch_delay=4, nsnake=12):
    d = Design("closed")
    d.fill(0,0,0,2,2,0,"stone")
    for y in range(3):
        d.set(-2,y,0,"sticky_piston",facing="east",extended=True)
        d.set(-1,y,0,"piston_head",facing="east",type="sticky")
        d.set(4,y,0,"sticky_piston",facing="west",extended=True)
        d.set(3,y,0,"piston_head",facing="west",type="sticky")
    d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone"); d.set(0,3,0,"stone")
    d.set(1,-2,0,"sticky_piston",facing="up")
    chain = [((-2,-1,0),"up"), ((-2,-2,0),"up"), ((-2,-2,1),"north"), ((-1,-2,1),"west"),
             ((0,-2,1),"west"), ((1,-2,1),"west"), ((2,-2,1),"west"), ((3,-2,1),"west"),
             ((4,-2,1),"west"), ((4,-2,0),"south"), ((3,-2,0),"east"), ((2,-2,0),"east")]
    for pos, f in chain:
        d.set(*pos,"observer",facing=f)
    # top mechanics
    d.set(1,5,0,"sticky_piston",facing="down")
    d.set(1,4,0,"sticky_piston",facing="down")
    d.set(3,3,0,"sticky_piston",facing="west")
    d.set(-1,3,0,"obsidian")
    # west: A pulse stretcher + relay
    d.set(0,4,0,"observer",facing="west")
    d.set(-1,4,0,"observer",facing="up")
    d.set(-1,5,0,"repeater",facing="west",delay=4)
    d.set(0,5,0,"stone")
    d.set(-2,4,0,"glass"); d.set(-2,5,0,"redstone_wire")
    d.set(-2,5,1,"stone")
    d.set(-2,4,1,"observer",facing="down")
    # west torch (alt config)
    d.set(-1,3,1,"stone"); d.set(-1,4,1,"redstone_wire")
    d.set(-2,3,1,"redstone_wall_torch",facing="west")
    d.set(-2,1,1,"stone"); d.set(-2,2,1,"redstone_wire")
    # arch
    d.set(0,4,1,"redstone_wire")
    d.set(1,4,1,"repeater",facing="east",delay=arch_delay)
    d.set(2,4,1,"redstone_wire"); d.set(3,3,1,"redstone_wire")
    d.set(2,5,1,"stone"); d.set(2,6,1,"lever",face="floor",facing="north")
    # east torch
    d.set(4,2,1,"redstone_wall_torch",facing="east")
    d.set(4,0,1,"stone"); d.set(4,1,1,"redstone_wire")
    # east: S chain (double pulse) + echo observer
    d.set(3,4,1,"observer",facing="west")
    d.set(4,4,1,"stone"); d.set(4,5,1,"redstone_wire")
    d.set(4,4,0,"glass"); d.set(4,5,0,"redstone_wire")
    d.set(3,5,0,"repeater",facing="east",delay=2)
    d.set(3,4,0,"observer",facing="up")
    d.set(2,4,0,"observer",facing="east")
    return d
d3 = build3()
d3.save("d3.json")
print(trace(d3, flips=2, limit=0))
print(trace(d3, flips=2, grep="(1,", limit=160))
