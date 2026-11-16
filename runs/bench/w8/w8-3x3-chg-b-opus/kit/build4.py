from pdbuild import Design
S="stone"
def build():
    d=Design("open")
    # top: lever + dust line on top pistons
    d.set(-1,4,0,S); d.set(-2,4,0,"lever",face="wall",facing="west")
    d.set(-2,3,0,"observer",facing="up"); d.set(-2,2,0,S)
    d.set(-1,5,0,"redstone_wire")
    for x in range(3):
        d.set(x,4,0,"sticky_piston",facing="down"); d.set(x,5,0,"redstone_wire"); d.set(x,3,0,S)
    d.set(3,4,0,S); d.set(3,5,0,"redstone_wire")
    d.set(4,3,0,"observer",facing="up"); d.set(4,4,0,"redstone_wire"); d.set(4,2,0,S)
    # sides
    for y in (0,1):
        d.set(-2,y,0,"sticky_piston",facing="east"); d.set(-1,y,0,S)
        d.set(4,y,0,"sticky_piston",facing="west"); d.set(3,y,0,S)
    d.set(-1,2,0,S); d.set(3,2,0,S); d.set(2,-1,0,S)
    # center
    d.set(0,-1,0,S); d.set(1,-1,0,S)
    d.set(-1,-1,0,"sticky_piston",facing="east")
    d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(1,-3,0,"sticky_piston",facing="up")
    # e1
    d.set(4,-1,0,"observer",facing="up")
    d.set(3,-1,0,"observer",facing="east")
    d.set(2,-2,0,"note_block")
    # e6 helper
    d.set(2,-3,0,"observer",facing="west"); d.set(3,-3,0,S); d.set(3,-2,0,"redstone_wire")
    # left chain
    d.set(-2,-1,0,"observer",facing="up"); d.set(-2,-2,0,"observer",facing="up"); d.set(-2,-3,0,"observer",facing="up")
    d.set(-1,-3,0,"observer",facing="west")
    d.set(-1,-2,0,"observer",facing="down")
    d.set(0,-4,0,S); d.set(0,-3,0,"repeater",facing="west",delay="3")
    d.set(0,-2,0,"observer",facing="down")
    return d
if __name__=="__main__":
    build().save("d4.json")
