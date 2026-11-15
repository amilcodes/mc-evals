def rowgroup(d):
    # left row units rows 1,2 + corner singles, open state
    for y in (1,2):
        d.set(-3,y,0,"sticky_piston",facing="east")
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(-1,y,0,"stone")
    for y in (0,3):
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(-1,y,0,"stone")
    # P structure back side
    d.set(-2,2,1,"stone"); d.set(-2,3,1,"redstone_wire")
    d.set(-3,2,1,"glass"); d.set(-3,3,1,"redstone_wire")
    d.set(-4,1,1,"stone"); d.set(-4,2,1,"redstone_wire")
    d.set(-3,0,1,"glass"); d.set(-3,1,1,"redstone_wire")
    d.set(-2,0,1,"glass"); d.set(-2,1,1,"redstone_wire")
    return d
d=Design()
rowgroup(d)
# pulse source
d.set(-8,1,1,"stone"); d.set(-8,2,1,"lever",face="floor",facing="north")
d.set(-7,1,1,"stone"); d.set(-7,2,1,"redstone_wire")
d.set(-6,2,1,"observer",facing="west")
d.set(-5,1,1,"stone"); d.set(-5,2,1,"redstone_wire")
# A lever: repeater at (-3,2,-1) facing north fed by lever block
d.set(-3,1,-1,"stone"); d.set(-3,2,-1,"redstone_wire")
d.set(-3,1,-2,"stone"); d.set(-3,2,-2,"redstone_wire")
d.set(-3,1,-3,"stone"); d.set(-3,2,-3,"lever",face="floor",facing="north")
lab=Lab(d,walls=True)
print(lab.lost)
def P():
    lab.flip(-8,2,1); lab.rest()
def A():
    lab.flip(-3,2,-3); lab.rest()
def show(tag):
    print(tag, {p:s.split('[')[0] for p,s in lab.blocks().items() if p[2]==0 and p[0]>=-3})
P(); show("P1")
A(); show("A")
P(); show("P2")
print(lab.doorway(), lab.entity)
P(); show("oP1"); A(); show("oA"); P(); show("oP2")
print(lab.doorway(), lab.entity)
