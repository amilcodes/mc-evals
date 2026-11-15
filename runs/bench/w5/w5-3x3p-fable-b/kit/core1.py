def core():
    d = Design()
    d.set(1,5,0,"sticky_piston",facing="down")
    d.set(1,4,0,"sticky_piston",facing="down")
    d.set(1,3,0,"stone"); d.set(0,3,0,"stone"); d.set(2,3,0,"stone")
    d.set(-1,3,0,"sticky_piston",facing="east")
    d.set(2,4,0,"redstone_wire")
    d.set(3,3,0,"glass"); d.set(3,4,0,"redstone_wire")
    d.set(3,4,1,"observer",facing="south")
    d.set(3,3,2,"stone"); d.set(3,4,2,"redstone_wire")
    d.set(4,3,2,"stone"); d.set(4,4,2,"lever",face="floor",facing="north")   # pulse lever
    d.set(1,5,1,"stone"); d.set(1,5,2,"lever",face="wall",facing="south")    # P1 lever
    d.set(-2,3,0,"stone"); d.set(-3,3,0,"lever",face="wall",facing="west")   # feeder lever
    # bottom single
    d.set(1,-2,0,"sticky_piston",facing="up"); d.set(1,-1,0,"stone")
    d.set(1,-2,1,"stone"); d.set(1,-2,2,"lever",face="wall",facing="south")
    return d
PUL=(4,4,2); P1L=(1,5,2); FL=(-3,3,0); BL=(1,-2,2)
def col(lab):
    return " ".join(f"{y}:{lab.block(1,y,0).split('[')[0][:10]}" for y in (5,4,3,2,1,0,-1))+" | (0,3):"+lab.block(0,3,0)[:12]
def act(lab, lever, n=8, show=True):
    s=len(lab.history)
    lab.flip(*lever); lab.step(n)
    if show:
        for t,pos,b,a in lab.history[s:]:
            if pos[2]==0 and pos[0] in (0,1,2) : print("  ",t,pos,b[:40],"->",a[:40])
    print(lab.t, col(lab), "entity", lab.entity)
lab=Lab(core(), walls=True)
print(lab.lost)
print(col(lab))
print("bottom close"); act(lab,BL,6,False)
print("pulse1"); act(lab,PUL,10)
