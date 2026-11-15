def build4():
    d = Design("closed")
    d.fill(0,0,0,2,2,0,"stone")
    for y in range(3):
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(4,y,0,"sticky_piston",facing="west")
    d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone"); d.set(0,3,0,"stone")
    d.set(-1,3,0,"obsidian")
    d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(1,5,0,"sticky_piston",facing="down")
    d.set(1,4,0,"sticky_piston",facing="down")
    d.set(3,3,0,"sticky_piston",facing="west")
    def ob(x,y,f): d.set(x,y,0,"observer",facing=f)
    # west unit
    ob(0,4,"west"); ob(-1,4,"up")
    d.set(-1,5,0,"repeater",facing="west",delay=4)
    d.set(0,5,0,"stone")
    ob(-2,5,"west")
    # east unit
    ob(2,4,"east"); ob(3,4,"up")
    d.set(3,5,0,"repeater",facing="east",delay=2)
    ob(4,5,"east")
    # side observers
    ob(4,4,"up"); ob(4,3,"up")
    ob(4,-2,"east"); ob(4,-1,"down")
    ob(-2,4,"up"); ob(-2,3,"up")
    # east column
    ob(5,-2,"east")
    d.set(6,-2,0,"lever",face="wall",facing="east")
    for y in range(-1,7): ob(5,y,"down")
    # row 6
    for x in range(4,-4,-1): ob(x,6,"east")
    # west column
    for y in range(5,-3,-1): ob(-3,y,"up")
    # bottom
    ob(-2,-2,"west"); ob(-2,-1,"down"); ob(-1,-1,"west"); ob(-1,-2,"up"); ob(0,-2,"west")
    return d
d4 = build4()
d4.save("d4.json")
print(trace(d4, flips=2, limit=0))
