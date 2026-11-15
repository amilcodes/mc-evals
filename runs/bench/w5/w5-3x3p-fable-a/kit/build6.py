def build6():
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
    # east unit; (4,5) is the start observer watching the lever
    ob(2,4,"east"); ob(3,4,"up")
    d.set(3,5,0,"repeater",facing="east",delay=2)
    ob(4,5,"east")
    d.set(5,5,0,"lever",face="wall",facing="east")
    # side observers
    ob(4,4,"up"); ob(4,3,"up")
    ob(-2,4,"up"); ob(-2,3,"up")
    # row 6 going west, piston relay over the DPE
    ob(4,6,"down"); ob(3,6,"east")
    d.set(2,6,0,"piston",facing="down")
    for x in range(1,-4,-1): ob(x,6,"east")
    # west column tail
    for y in range(5,-3,-1): ob(-3,y,"up")
    ob(-2,-2,"west"); ob(-2,-1,"down"); ob(-1,-1,"west"); ob(-1,-2,"up"); ob(0,-2,"west")
    # east bottom: from Pb to the right-bottom piston
    ob(2,-2,"west"); ob(3,-2,"west"); ob(4,-2,"west"); ob(4,-1,"down")
    return d
d6 = build6()
d6.save("d6.json")
print(trace(d6, flips=2, limit=0))
