def core():
    d = Design("open")
    S="stone"
    # left / right columns
    for y in range(3):
        d.set(-2,y,0,"sticky_piston",facing="east"); d.set(-1,y,0,S)
        d.set(4,y,0,"sticky_piston",facing="west"); d.set(3,y,0,S)
    # top
    d.set(1,4,0,"sticky_piston",facing="down"); d.set(1,3,0,S)
    d.set(0,3,0,S); d.set(2,3,0,S)
    # mechanism
    d.set(0,-1,0,S)            # F
    d.set(1,-1,0,S)            # A
    d.set(2,-1,0,S)            # N
    d.set(3,-1,0,"sticky_piston",facing="west")   # W'
    d.set(1,-2,0,"sticky_piston",facing="up")     # P2
    d.set(1,-3,0,"sticky_piston",facing="up")     # P1
    return d

d = core()
# S2 feed: Bk strongly powered -> repeater -> F ; test lever on Bk
d.set(-2,-1,0,S:="stone")
d.set(-1,-2,0,"stone"); d.set(-1,-1,0,"repeater",facing="west",delay=1)
d.set(0,-3,0,"glass"); d.set(0,-2,0,"redstone_wire")
# lever for S2 on Bk from south side
d.set(-2,-1,1,"lever",face="wall",facing="south")
# S1: block (2,-3) with dust on top fed from z=1
d.set(2,-3,0,"stone"); d.set(2,-2,0,"redstone_wire")
d.set(2,-3,1,"stone"); d.set(2,-2,1,"redstone_wire")
d.set(2,-3,2,"stone"); d.set(2,-2,2,"lever",face="floor",facing="north")
# W' lever below
d.set(4,-1,0,"stone"); d.set(4,-1,1,"lever",face="wall",facing="south")
lab = Lab(d, walls=True)
print(lab.lost)
S2=(-2,-1,1); S1=(2,-2,2); SW=(4,-1,1)
def do(lv, n=6):
    lab.flip(*lv); ch=lab.step(n)
    print(lab.doorway(), [lab.block(1,y,0)[:24] for y in (-3,-2,-1)], lab.block(2,-1,0)[:20], lab.block(-2,0,0)[-15:], lab.entity)
# closing: S2 short pulse
lab.flip(*S2); lab.step(2); lab.flip(*S2); lab.step(6)
print(lab.doorway(), [lab.block(1,y,0)[:24] for y in (-3,-2,-1,0)], lab.entity)
do(SW); do(S2)
print("closed?", lab.doorway())
# opening
do(S2); do(SW); do(S1); do(S2,4); do(S2,4); do(S1); do(S2,4); do(S2,4)
print(lab.view(z=0))
