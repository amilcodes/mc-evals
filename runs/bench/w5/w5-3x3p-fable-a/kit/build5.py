def build5():
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
    ob(4,-2,"down"); ob(4,-1,"down")
    ob(-2,4,"up"); ob(-2,3,"up")
    # start
    ob(3,-3,"south")
    d.set(3,-3,1,"lever",face="wall",facing="south")
    # east branch
    ob(4,-3,"west"); ob(5,-3,"west")
    for y in range(-2,6): ob(5,y,"down")
    # west branch
    for x in range(2,-5,-1): ob(x,-3,"east")
    for y in range(-2,6): ob(-4,y,"down")
    ob(-3,5,"west")
    # tail
    for y in range(4,-3,-1): ob(-3,y,"up")
    ob(-2,-2,"west"); ob(-2,-1,"down"); ob(-1,-1,"west"); ob(-1,-2,"up"); ob(0,-2,"west")
    return d
d5 = build5()
d5.save("d5.json")
print(trace(d5, flips=2, limit=0))
