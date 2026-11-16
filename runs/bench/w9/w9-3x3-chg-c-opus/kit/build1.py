def build():
    d=Design("closed")
    S=lambda x,y,z,b,**p: d.set(x,y,z,b,**p)
    for x in range(3):
        for y in range(3): S(x,y,0,"stone")
    for y in range(3):
        S(-2,y,0,"sticky_piston",facing="east"); S(4,y,0,"sticky_piston",facing="west")
    S(1,-2,0,"sticky_piston",facing="up")
    S(0,-1,0,"stone"); S(2,-1,0,"stone"); S(2,3,0,"stone")
    S(-1,3,0,"sticky_piston",facing="east")      # K
    S(1,4,0,"sticky_piston",facing="down")       # F
    S(1,5,0,"sticky_piston",facing="down")       # B
    S(1,6,0,"glass"); S(1,7,0,"redstone_wire")
    S(2,6,0,"stone"); S(2,7,0,"redstone_wire"); S(2,5,0,"glass")
    S(3,5,0,"observer",facing="up"); S(3,6,0,"redstone_wire")
    S(4,5,0,"stone"); S(4,6,0,"redstone_wire")
    S(5,5,0,"stone"); S(5,6,0,"redstone_wire")
    S(3,3,0,"glass"); S(3,4,0,"redstone_wire")   # X
    S(2,4,0,"observer",facing="east")            # OF
    S(4,4,0,"observer",facing="east")            # R0
    S(5,4,0,"lever",face="wall",facing="east")
    S(4,3,0,"observer",facing="up")              # D_R2
    S(-1,4,0,"observer",facing="up")             # OK
    S(-1,5,0,"observer",facing="south")          # V
    S(0,4,0,"observer",facing="west")            # F1obs
    # gate
    S(5,4,1,"sticky_piston",facing="up"); S(5,5,1,"stone")
    S(6,6,1,"repeater",facing="east",delay=4); S(6,5,1,"stone")
    S(7,6,1,"observer",facing="east"); S(8,6,1,"observer",facing="up")
    S(8,7,1,"observer",facing="west"); S(7,7,1,"observer",facing="west")
    S(6,7,1,"observer",facing="west"); S(5,7,1,"observer",facing="west")
    S(4,7,1,"observer",facing="down"); S(4,6,1,"observer",facing="down")
    # K / top chain
    S(4,4,1,"observer",facing="north"); S(4,5,1,"observer",facing="down")
    for x in range(-1,4): S(x,5,1,"observer",facing="east")
    S(-2,5,1,"observer",facing="east"); S(-2,4,1,"observer",facing="up")
    S(-2,4,0,"observer",facing="south"); S(-2,3,0,"observer",facing="up")
    # right/bottom chain
    for y in range(-2,4): S(4,y,1,"observer",facing="up")
    S(4,-2,0,"observer",facing="south"); S(4,-1,0,"observer",facing="down")
    for x in range(-2,4): S(x,-2,1,"observer",facing="east")
    S(-1,-2,0,"observer",facing="south"); S(0,-2,0,"observer",facing="west")
    S(-2,-2,0,"observer",facing="south"); S(-2,-1,0,"observer",facing="down")
    return d
d1=build(); d1.save("d1.json")
