from pdbuild import Design

def top_pair(d):
    # top I lanes cols 1,2
    for x in (1,2):
        d.set(x,6,0,"sticky_piston",facing="down")
        d.set(x,5,0,"sticky_piston",facing="down")
        d.set(x,4,0,"stone")
        d.set(x,5,1,"observer",facing="south")   # Oh: out north into home; displaced by QC
        d.set(x,6,1,"stone")                      # powers P1
    for x in (0,1,2,3):
        d.set(x,5,2,"redstone_wire")              # D1 on walls
    for sx,gx,cx in ((-1,0,-1),(4,3,4)):
        d.set(cx,4,2,"stone"); d.set(cx,5,2,"redstone_wire")
        d.set(cx,4,1,"stone"); d.set(cx,5,1,"redstone_wire")
        d.set(gx,5,1,"glass"); d.set(gx,6,1,"redstone_wire")
        d.set(gx,6,2,"stone")   # cuts the step from (gx,5,2) up to (gx,6,1)
    return d

def run(lab, lever, show=lambda pos: pos[2]==0):
    start=lab.t; seen=len(lab.history)
    lab.flip(*lever); ok=lab.rest()
    for t,pos,b,a in lab.history[seen:]:
        if show(pos): print(f"  +{t-start:<3} {pos} {b} -> {a}")
    print("rest",ok,"entity",lab.entity)

def left_side(d, taps=True):
    """Left half lanes (x<0) + left bottom lanes. taps=False leaves trigger supports as stone."""
    # ---- row 3 (O lane): delivers (1,3) via (0,3)
    d.set(-3,3,0,"sticky_piston",facing="east"); d.set(-2,3,0,"sticky_piston",facing="east"); d.set(-1,3,0,"stone")
    d.set(-3,2,1,"stone"); d.set(-3,3,1,"repeater",facing="south",delay=4)
    d.set(-2,3,1,"observer",facing="west")            # Od -> wall (-1,3,1) -> displaced
    d.set(-3,4,0,"observer",facing="west")            # Oh -> air (-2,4,0) -> home via QC
    d.set(-4,3,0,"glass"); d.set(-4,4,0,"repeater",facing="south",delay=4)
    d.set(-4,3,1,"stone"); d.set(-4,4,1,"redstone_wire")
    d.set(-4,3,2,"redstone_wire")                     # on (-4,2,2)
    d.set(-3,2,2,"stone"); d.set(-3,3,2,"redstone_wire")
    # ---- row 0 (O lane): delivers (1,0) via (0,0)
    d.set(-3,0,0,"sticky_piston",facing="east"); d.set(-2,0,0,"sticky_piston",facing="east"); d.set(-1,0,0,"stone")
    d.set(-3,-1,1,"stone"); d.set(-3,0,1,"repeater",facing="south",delay=4)
    d.set(-2,0,1,"observer",facing="west")            # Od -> wall (-1,0,1)
    d.set(-2,-1,0,"observer",facing="down")           # Oh -> up into home
    d.set(-2,-3,0,"stone"); d.set(-2,-2,0,"repeater",facing="south",delay=4)
    d.set(-3,0,2,"redstone_wire")                     # on (-3,-1,2)
    d.set(-2,-2,2,"stone"); d.set(-2,-1,2,"redstone_wire")
    d.set(-2,-3,1,"stone"); d.set(-2,-2,1,"redstone_wire")
    # ---- rows 1,2 (F singles); F2 toggled by observer, F1 by QC
    d.set(-2,2,0,"sticky_piston",facing="east"); d.set(-1,2,0,"stone")
    d.set(-2,1,0,"sticky_piston",facing="east"); d.set(-1,1,0,"stone")
    d.set(-2,2,1,"observer",facing="south")
    # ---- bottom: col 0 C single, col 1 I lane
    d.set(0,-2,0,"sticky_piston",facing="up"); d.set(0,-1,0,"stone")
    d.set(0,-2,1,"observer",facing="south")
    d.set(1,-3,0,"sticky_piston",facing="up"); d.set(1,-2,0,"sticky_piston",facing="up"); d.set(1,-1,0,"stone")
    d.set(1,-4,1,"stone"); d.set(1,-3,1,"repeater",facing="south",delay=4)
    d.set(1,-2,1,"observer",facing="down")
    d.set(1,-3,2,"redstone_wire")                     # on (1,-4,2)
    # ---- top: col 0 C single (toggled from the west)
    d.set(0,5,0,"sticky_piston",facing="down"); d.set(0,4,0,"stone")
    d.set(-1,5,0,"observer",facing="west")
    if not taps:
        d.set(-4,2,2,"stone"); d.set(-3,-1,2,"stone"); d.set(1,-4,2,"stone")
    return d
