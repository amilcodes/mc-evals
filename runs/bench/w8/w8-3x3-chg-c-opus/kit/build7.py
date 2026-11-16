def build7(gd=1):
    d = Design("open")
    S = d.set
    for y in range(3):
        S(-2,y,0,"sticky_piston",facing="east"); S(-1,y,0,"stone")
        S(4,y,0,"sticky_piston",facing="west"); S(3,y,0,"stone")
    S(1,-2,0,"sticky_piston",facing="up"); S(1,-1,0,"stone"); S(0,-1,0,"stone"); S(2,-1,0,"stone")
    S(0,3,0,"stone"); S(1,3,0,"stone"); S(2,3,0,"stone")
    S(1,4,0,"sticky_piston",facing="down"); S(1,5,0,"sticky_piston",facing="down")
    S(3,3,0,"sticky_piston",facing="west")
    S(0,4,-2,"lever",face="floor",facing="north")
    S(0,4,-1,"repeater",facing="north",delay=1)
    S(0,4,0,"repeater",facing="west",delay=gd)
    S(-1,4,0,"stone"); S(-1,5,0,"redstone_wire"); S(0,5,0,"observer",facing="east")  # W
    S(1,5,-1,"stone"); S(4,3,0,"stone")
    O = [((1,4,-1),"west"),((2,4,-1),"west"),((3,4,-1),"west"),((3,4,0),"north"),((2,4,0),"east"),
         ((4,4,-1),"west"),((4,5,-1),"down"),((4,5,0),"north"),((4,4,0),"up"),
         ((3,5,0),"east"),((3,5,-1),"south"),((2,5,-1),"east"),
         ((4,3,-1),"up"),((4,2,-1),"up"),((4,1,-1),"up"),((4,0,-1),"up"),((4,-1,-1),"up"),((4,-2,-1),"up"),
         ((3,-2,-1),"east"),((2,-2,-1),"east"),((1,-2,-1),"east"),((0,-2,-1),"east"),((-1,-2,-1),"east"),((-2,-2,-1),"east"),
         ((-2,-1,-1),"down"),((-2,0,-1),"down"),((-2,1,-1),"down"),((-2,2,-1),"down"),((-2,3,-1),"down"),((-2,4,-1),"down"),
         ((-1,4,-1),"west"),((-1,5,-1),"down"),((0,5,-1),"west"),
         ((4,-2,0),"north"),((4,-1,0),"down"),((3,-2,0),"north"),((2,-2,0),"east"),
         ((-2,-2,0),"north"),((-2,-1,0),"down"),((-2,4,0),"north"),((-2,3,0),"up")]
    for p,f in O: S(*p,"observer",facing=f)
    return d
