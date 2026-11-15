def build3():
    d = Design("closed")
    for x in range(3):
        for y in range(3): d.set(x,y,0,"stone")
    for p in [(0,-1,0),(2,-1,0),(2,3,0)]: d.set(*p,"stone")
    for y in range(3):
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(4,y,0,"sticky_piston",facing="west")
    d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(-1,3,0,"sticky_piston",facing="east")
    d.set(1,4,0,"sticky_piston",facing="down")
    d.set(1,5,0,"sticky_piston",facing="down")
    d.set(-2,3,0,"stone")                       # K/TL block
    d.set(1,4,2,"lever",face="wall",facing="south")
    # R_C
    d.set(-1,4,0,"stone"); d.set(-1,5,0,"repeater",facing="south",delay=4)
    d.set(-1,4,1,"glass"); d.set(-1,5,1,"redstone_wire")
    # R_B
    d.set(3,3,0,"stone"); d.set(3,4,0,"repeater",facing="east",delay=4)
    d.set(4,3,0,"stone"); d.set(4,4,0,"redstone_wire")
    d.set(4,3,1,"glass"); d.set(4,4,1,"redstone_wire")
    chain = [
      ((1,4,1),(1,4,2)),                          # X -> E1
      ((1,5,1),(1,4,1)), ((0,5,1),(1,5,1)),       # -> dust (-1,5,1) -> R_C
      ((2,5,1),(1,5,1)), ((2,4,1),(2,5,1)), ((3,4,1),(2,4,1)),  # -> dust (4,4,1) -> R_B, TR/MR
      ((0,5,0),(-1,5,0)), ((2,4,0),(3,4,0)),      # C', B
      ((-2,5,1),(-1,5,1)), ((-2,5,0),(-2,5,1)), ((-2,4,0),(-2,5,0)),   # K
      ((-2,4,1),(-2,5,1)), ((-2,3,1),(-2,4,1)), ((-2,2,1),(-2,3,1)),
      ((-2,1,1),(-2,2,1)), ((-2,0,1),(-2,1,1)), ((-2,-1,1),(-2,0,1)), ((-2,-2,1),(-2,-1,1)),
      ((-2,-2,0),(-2,-2,1)), ((-2,-1,0),(-2,-2,0)),   # BL
      ((-1,-2,1),(-2,-2,1)), ((0,-2,1),(-1,-2,1)), ((1,-2,1),(0,-2,1)), ((2,-2,1),(1,-2,1)),
      ((3,-2,1),(2,-2,1)), ((4,-2,1),(3,-2,1)), ((4,-2,0),(4,-2,1)), ((4,-1,0),(4,-2,0)),  # BR
      ((3,-2,0),(4,-2,0)), ((2,-2,0),(3,-2,0)),   # BM
    ]
    for p,w in chain: obs(d,p,w)
    return d
