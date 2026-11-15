def build1():
    d = Design("closed")
    # door stones
    d.fill(0,0,0,2,2,0,"stone")
    # side pistons, extended
    for y in range(3):
        d.set(-2,y,0,"sticky_piston",facing="east",extended=True)
        d.set(-1,y,0,"piston_head",facing="east",type="sticky")
        d.set(4,y,0,"sticky_piston",facing="west",extended=True)
        d.set(3,y,0,"piston_head",facing="west",type="sticky")
    # frame statics
    d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone"); d.set(0,3,0,"stone")
    # bottom
    d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(-1,-1,0,"observer",facing="up")
    d.set(-1,-2,0,"note_block")
    d.set(0,-2,0,"observer",facing="west")
    # top mechanics
    d.set(1,5,0,"sticky_piston",facing="down")
    d.set(1,4,0,"sticky_piston",facing="down")
    d.set(3,3,0,"sticky_piston",facing="west")
    d.set(0,4,0,"observer",facing="west")
    d.set(2,4,0,"observer",facing="east")
    d.set(3,4,0,"observer",facing="up")
    d.set(3,5,0,"observer",facing="south")
    d.set(-1,3,0,"glass"); d.set(-1,4,0,"redstone_wire")
    d.set(0,5,0,"stone")   # A-stone
    # z=1 arch
    d.set(0,5,1,"stone"); d.set(0,6,1,"lever",face="floor",facing="north")
    d.set(-1,3,1,"redstone_wire"); d.set(0,4,1,"redstone_wire")
    d.set(1,4,1,"repeater",facing="west",delay=1)
    d.set(2,4,1,"redstone_wire"); d.set(3,3,1,"redstone_wire")
    d.set(3,4,1,"glass"); d.set(3,5,1,"redstone_wire")
    d.set(4,3,1,"glass"); d.set(4,4,1,"redstone_wire")
    # side torches
    d.set(-2,2,1,"redstone_wall_torch",facing="west")
    d.set(-2,0,1,"stone"); d.set(-2,1,1,"redstone_wire")
    d.set(4,2,1,"redstone_wall_torch",facing="east")
    d.set(4,0,1,"stone"); d.set(4,1,1,"redstone_wire")
    # delay + comparator logic
    d.set(4,3,0,"glass"); d.set(4,4,0,"repeater",facing="south",delay=4)
    d.set(4,3,-1,"glass"); d.set(4,4,-1,"redstone_wire")
    d.set(4,3,-2,"glass"); d.set(4,4,-2,"redstone_wire")
    d.set(3,3,-2,"glass"); d.set(3,4,-2,"redstone_wire")
    d.set(3,3,-1,"glass"); d.set(3,4,-1,"repeater",facing="east",delay=3)
    d.set(2,4,-1,"redstone_wire")
    d.set(2,4,-2,"comparator",facing="east",mode="subtract")
    d.set(1,4,-2,"redstone_wire"); d.set(0,4,-2,"redstone_wire")
    d.set(0,4,-1,"stone"); d.set(0,5,-1,"redstone_wire")
    d.set(1,4,-1,"observer",facing="north")
    return d
d1 = build1()
d1.save("d1.json")
r = test(d1)
print(r)
