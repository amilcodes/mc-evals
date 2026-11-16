def build():
    d = Design("open")
    S = d.set
    # mechanism z=0
    for y in range(3):
        S(-2,y,0,"sticky_piston",facing="east"); S(-1,y,0,"stone")
        S(4,y,0,"sticky_piston",facing="west"); S(3,y,0,"stone")
    S(1,-2,0,"sticky_piston",facing="up"); S(1,-1,0,"stone"); S(0,-1,0,"stone"); S(2,-1,0,"stone")
    S(0,3,0,"stone"); S(1,3,0,"stone"); S(2,3,0,"stone")
    S(1,4,0,"sticky_piston",facing="down"); S(1,5,0,"sticky_piston",facing="down")
    S(3,3,0,"sticky_piston",facing="west")
    # lever + left
    S(-2,1,-1,"lever",face="ceiling",facing="north"); S(-2,2,-1,"stone")
    # SB chain
    S(-2,-1,-1,"stone"); S(-2,0,-1,"redstone_wire")
    S(-2,-2,0,"stone"); S(-2,-1,0,"redstone_wire")
    S(-1,-2,0,"note_block"); S(-1,-1,0,"redstone_wire")
    S(0,-2,0,"observer",facing="west")
    # bus
    for p in [(-2,3,-1),(-1,3,-1),(-1,3,-2),(0,4,-2),(1,4,-2),(2,4,-2),(3,3,-2),(4,2,-2),(4,2,-1)]:
        S(*p,"redstone_wire")
    S(4,1,-2,"stone"); S(4,1,-1,"stone")
    # gate
    S(0,4,-1,"repeater",facing="north",delay=1)
    S(0,4,0,"comparator",facing="west",mode="subtract")
    S(1,4,-1,"observer",facing="north")   # E1
    S(-1,4,0,"observer",facing="west")    # comp rear
    S(-2,3,0,"glass"); S(-2,4,0,"redstone_wire")
    S(-2,3,1,"glass"); S(-2,4,1,"redstone_wire")
    S(-2,4,-1,"observer",facing="north")  # FA
    S(-1,4,1,"observer",facing="east")    # FB
    # Pb emitters
    S(2,5,0,"observer",facing="east"); S(0,5,0,"observer",facing="west")
    S(3,5,0,"observer",facing="north"); S(-1,5,0,"observer",facing="up")
    # R emitter
    S(3,4,1,"observer",facing="up"); S(3,3,1,"stone")
    # snake
    snake = [((2,5,-2),"down"),((3,5,-2),"west"),((4,5,-2),"west"),((4,4,-2),"up"),((4,4,-1),"north"),
             ((4,4,0),"north"),((4,4,1),"north"),((4,5,1),"down"),((3,5,1),"east"),((2,5,1),"east"),
             ((2,4,1),"up"),((2,4,0),"south"),((3,4,0),"west"),((3,4,-1),"south"),((3,5,-1),"down"),
             ((2,5,-1),"east"),((1,5,-1),"east"),((0,5,-1),"east"),((-1,5,-1),"east"),((-2,5,-1),"east"),
             ((-2,5,-2),"south"),((-2,4,-2),"up"),
             ((-2,6,-1),"down"),((-1,6,-1),"west"),((0,6,-1),"west"),((0,6,0),"north"),((-1,6,0),"east"),
             ((0,6,1),"north"),((0,5,1),"up"),((0,4,1),"up")]
    for p,f in snake: S(*p,"observer",facing=f)
    return d
