def core():
    d = Design("open")
    # DPE on top
    d.set(1,5,0,"sticky_piston",facing="down")
    d.set(1,4,0,"sticky_piston",facing="down")
    d.set(1,3,0,"stone")   # U
    d.set(2,3,0,"stone")   # T
    d.set(3,3,0,"sticky_piston",facing="west")  # E
    d.set(0,3,0,"stone")
    # bottom
    d.set(1,-2,0,"sticky_piston",facing="up"); d.set(1,-1,0,"stone")
    d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone")
    # observer on P1 -> P2 dust
    d.set(1,5,1,"observer",facing="north")
    d.set(1,5,2,"stone")
    d.set(1,4,2,"redstone_wire")
    d.set(1,4,1,"redstone_wire")
    return d
d = core()
# manual levers: P1 via stone at (0,5,0) w/ lever on top; E via lever at (3,4,0)?; B via lever
d.set(0,5,0,"stone"); d.set(0,6,0,"lever",face="floor",facing="north")
d.set(4,3,0,"stone"); d.set(4,4,0,"lever",face="floor",facing="north")
d.set(0,-2,0,"stone"); d.set(0,-3,0,"lever",face="ceiling",facing="north")
lab = Lab(d, walls=True)
print(lab.lost)
P1L=(0,6,0); EL=(4,4,0); BL=(0,-3,0)
def col():
    return {y: lab.block(1,y,0) for y in range(5,-3,-1)}, lab.block(2,3,0), lab.block(0,3,0)
def go(lev, n=12):
    t0=lab.t
    lab.flip(*lev)
    ch = lab.step(n)
    for t,pos,b,a in ch:
        if pos[0] in (1,2,3) and pos[2]==0 and pos[1]>=0: print("  +%d %s %s -> %s"%(t-t0,pos,b,a))
    print(col(), lab.entity)
# closing sequence
print("B on"); go(BL,6)
print("P1 on"); go(P1L)
print("P1 off"); go(P1L)
print("E on"); go(EL,6)
print("P1 on"); go(P1L)
print(lab.doorway())
