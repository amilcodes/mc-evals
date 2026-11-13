def core():
    d = Design("open")
    # center mech
    d.set(1,-3,0,"sticky_piston",facing="up")   # P1
    d.set(1,-2,0,"sticky_piston",facing="up")   # P2
    d.set(1,-1,0,"stone")  # A
    d.set(0,-1,0,"stone")  # B
    d.set(-1,-1,0,"sticky_piston",facing="east")  # H
    d.set(2,-1,0,"stone")
    # P2 power: repeater into frame stone
    d.set(3,-2,0,"stone"); d.set(3,-1,0,"repeater",facing="east",delay=1)
    d.set(4,-2,0,"stone"); d.set(4,-1,0,"redstone_wire")
    d.set(4,-3,1,"stone"); d.set(4,-2,1,"redstone_wire")
    d.set(3,-3,1,"stone"); d.set(3,-2,1,"observer",facing="west")
    # P1 power
    d.set(2,-3,0,"stone"); d.set(2,-2,0,"redstone_wire")
    d.set(2,-3,1,"stone"); d.set(2,-2,1,"redstone_wire")
    d.set(2,-3,2,"stone"); d.set(2,-2,2,"redstone_wire")
    # H power
    d.set(-1,-2,0,"stone")
    d.set(-1,-3,1,"stone"); d.set(-1,-2,1,"redstone_wire")
    d.set(-1,-3,2,"stone"); d.set(-1,-2,2,"redstone_wire")
    return d
d = core()
# test levers
d.set(2,-3,3,"stone"); d.set(2,-2,3,"lever",face="floor",facing="north")
d.set(-1,-3,3,"stone"); d.set(-1,-2,3,"lever",face="floor",facing="north")
lab = Lab(d, walls=True)
print(lab.lost)
def show(msg):
    print(msg, lab.t, lab.doorway(), {p:lab.block(*p)[:22] for p in [(1,-3,0),(1,-2,0),(1,-1,0),(0,-1,0),(1,0,0),(1,1,0)]})
PL=(2,-2,3); HL=(-1,-2,3)
show("init")
lab.flip(*PL); lab.step(12); show("P1 on")
lab.flip(*PL); lab.step(12); show("P1 off")
lab.flip(*HL); lab.step(8); show("H on")
