def build5(gd=2):
    d = Design("open")
    S = d.set
    for y in range(3):
        S(-2,y,0,"sticky_piston",facing="east"); S(-1,y,0,"stone")
        S(4,y,0,"sticky_piston",facing="west"); S(3,y,0,"stone")
    S(1,-2,0,"sticky_piston",facing="up"); S(1,-1,0,"stone"); S(0,-1,0,"stone"); S(2,-1,0,"stone")
    S(0,3,0,"stone"); S(1,3,0,"stone"); S(2,3,0,"stone")
    S(1,4,0,"sticky_piston",facing="down"); S(1,5,0,"sticky_piston",facing="down")
    S(3,3,0,"sticky_piston",facing="west")
    S(-2,1,-1,"lever",face="ceiling",facing="north"); S(-2,2,-1,"stone")
    S(-2,-1,-1,"stone"); S(-2,0,-1,"redstone_wire")
    S(-2,-2,0,"stone"); S(-2,-1,0,"redstone_wire")
    S(-1,-2,0,"stone"); S(-1,-1,0,"redstone_wire")
    S(0,-2,0,"note_block")
    for p in [(-2,3,-1),(-1,3,-1),(-1,3,-2),(0,4,-2),(1,4,-2),(2,4,-2),(3,3,-2),(4,2,-2),(4,2,-1)]:
        S(*p,"redstone_wire")
    S(4,1,-2,"stone"); S(4,1,-1,"stone")
    S(0,4,-1,"repeater",facing="north",delay=1)
    S(0,4,0,"repeater",facing="west",delay=gd)
    S(-1,4,0,"stone"); S(-1,5,0,"redstone_wire"); S(0,5,0,"observer",facing="east")  # W
    S(1,4,-1,"observer",facing="north")  # E1
    S(3,4,0,"redstone_wire"); S(3,4,-1,"observer",facing="north"); S(3,4,-2,"observer",facing="down")
    S(3,5,0,"observer",facing="down"); S(2,5,0,"observer",facing="east")  # PbR
    for p,f in [((4,4,-2),"west"),((4,5,-2),"down"),((3,5,-2),"east"),((3,5,-1),"north"),((2,5,-1),"east"),((2,5,-2),"south"),((1,5,-2),"east"),((1,5,-1),"north")]:
        S(*p,"observer",facing=f)
    return d
