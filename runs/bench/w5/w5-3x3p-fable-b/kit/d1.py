def build(dB=1, d3=4, d1=3):
    d = Design("open")
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    W=lambda x,y,z: d.set(x,y,z,"redstone_wire")
    G=lambda x,y,z: d.set(x,y,z,"glass")
    # --- door singles
    for y in (0,1,2):
        S(-2,y,0,"sticky_piston",facing="east"); S(-1,y,0)
        S(4,y,0,"sticky_piston",facing="west"); S(3,y,0)
    S(1,-2,0,"sticky_piston",facing="up"); S(1,-1,0); S(0,-1,0); S(2,-1,0)
    # --- top module
    S(1,5,0,"sticky_piston",facing="down"); S(1,4,0,"sticky_piston",facing="down")
    S(1,3,0); S(0,3,0); S(2,3,0)
    S(-1,3,0,"sticky_piston",facing="east")
    W(2,4,0)                       # T
    S(3,4,0); W(3,5,0)             # T east-up connection
    # --- lever + bottom
    S(1,-2,1); S(1,-2,2,"lever",face="wall",facing="south")
    S(0,-3,1); W(0,-2,1); S(0,-3,2); W(0,-2,2)
    S(-1,-3,2); S(-1,-2,2,"repeater",facing="east",delay=d1)
    S(-2,-3,2); W(-2,-2,2)         # A0 (X)
    for x in (2,3,4): S(x,-3,1); W(x,-2,1)
    # --- left chain parity B (z: y=-2:2, -1:1, 0:2, 1:1, 2:2, 3:1, 4:2)
    for y,z in ((-1,1),(0,2),(1,1),(2,2),(3,1),(4,2)):
        G(-2,y-1,z); W(-2,y,z)
    S(-2,3,0)                      # powers feeder + left top piston
    # --- right chain parity A (y=-2:1, -1:2, 0:1, 1:2, 2:1, 3:2, 4:1)
    for y,z in ((-1,2),(0,1),(1,2),(2,1),(3,2),(4,1)):
        G(4,y-1,z); W(4,y,z)
    S(4,5,1)                       # cut block above A6'
    # --- top level 5 chain
    G(-2,4,1); W(-2,5,1); G(-2,4,0); W(-2,5,0)
    G(-1,4,0); S(-1,5,0,"repeater",facing="west",delay=d3)
    G(-1,4,1); S(-1,5,1,"repeater",facing="west",delay=dB)
    G(0,4,1); W(0,5,1)
    S(0,4,0); S(0,5,0,"comparator",facing="west",mode="subtract")
    # --- observers
    S(2,4,1)                                   # Q
    S(3,4,1,"observer",facing="east")          # Obs_L
    S(1,5,1,"observer",facing="west")          # Obs_S
    S(2,5,1)                                   # strong block
    W(3,5,1)
    S(2,5,0,"observer",facing="west")          # Obs_p
    return d
d=build(); d.save("d1.json")
r=test(d); print(r)
