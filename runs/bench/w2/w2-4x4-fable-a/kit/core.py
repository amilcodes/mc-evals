def left_core(state="open"):
    d = Design(state)
    for y in (1, 2):
        d.set(-3, y, 0, "sticky_piston", facing="east")
        d.set(-2, y, 0, "sticky_piston", facing="east")
    d.set(-1, 4, 0, "sticky_piston", facing="down")
    d.set(-1, -1, 0, "sticky_piston", facing="up")
    if state == "open":
        for y in (0, 1, 2, 3):
            d.set(-1, y, 0, "stone")
    # home observer
    d.set(-2, 3, 0, "observer", facing="up")
    d.set(-2, 4, 0, "repeater", facing="south")
    d.set(-2, 3, 1, "glass"); d.set(-2, 4, 1, "redstone_wire")
    # R dust and f observer
    d.set(-3, 1, 1, "stone"); d.set(-3, 2, 1, "redstone_wire")
    d.set(-2, 2, 1, "observer", facing="west")
    return d

def manual(d):
    d.set(-2, 4, 2, "stone"); d.set(-2, 5, 2, "lever", face="floor", facing="north")
    d.set(-3, 1, 2, "stone"); d.set(-3, 2, 2, "redstone_wire")
    d.set(-3, 1, 3, "stone"); d.set(-3, 2, 3, "repeater", facing="south")
    d.set(-3, 2, 4, "stone"); d.set(-3, 3, 4, "lever", face="floor", facing="north")
    d.set(-1, 5, 0, "stone"); d.set(-1, 6, 0, "lever", face="floor", facing="north")
    d.set(-1, -2, 0, "stone"); d.set(-1, -3, 0, "lever", face="ceiling", facing="north")
    return d
H=(-2,5,2); R=(-3,3,4); UT=(-1,6,0); UB=(-1,-3,0)
def show(lab, tag=""):
    print(tag, "t=%d"%lab.t, lab.doorway(), sorted((p[0],p[1],s.split('[')[0][:6]) for p,s in lab.blocks().items() if p[2]==0 and -3<=p[0]<=1 and -1<=p[1]<=4 and s!='air' and 'observer' not in s and 'repeater' not in s))
def act(lab, lev, n=12, verbose=False):
    t0=lab.t
    lab.flip(*lev)
    ch=lab.step(n)
    if verbose:
        for t,p,b,a in ch:
            if 'wire' not in a: print("   +%d"%(t-t0), p, b.split('[')[0], "->", a)
