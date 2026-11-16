exec(open("v1.py").read())
def build2(dk=1, dx=3, dline=(4,4,4,2), ys=1, wd=(4,4,4), wr=1, rd=4):
    d = build(dk=dk, dx=dx, dline=dline)
    S = d.set
    xe = -4-len(dline)
    # replace riser: remove old riser cells
    for p in list(d.blocks):
        if p[2]==-1 and p[1] in (-2,-1,0) and xe < p[0] < -3 and p not in [(-2,-2,-1)]:
            if d.blocks[p][0] in ("redstone_wire","glass"): d.remove(*p)
    S(-5,-1,-1,"redstone_wire"); S(-5,-2,-1,"glass")
    S(-4,0,-1,"redstone_wire"); S(-4,-1,-1,"glass")
    # window chain
    S(-3,0,-2,"observer",facing="east")
    S(-4,0,-2,"repeater",facing="east",delay=4); S(-4,-1,-2,"stone")
    S(-5,0,-2,"repeater",facing="east",delay=ys); S(-5,-1,-2,"stone")
    S(-6,0,-2,"redstone_wire"); S(-6,-1,-2,"stone")
    S(-7,0,-2,"redstone_wire"); S(-7,-1,-2,"stone")
    S(-7,0,-1,"redstone_wire"); S(-7,-1,-1,"stone")
    S(-7,0,0,"redstone_wire"); S(-7,-1,0,"stone")
    S(-6,1,0,"redstone_wire"); S(-6,0,0,"stone")
    S(-5,1,0,"redstone_wire"); S(-5,0,0,"stone")
    S(-5,1,1,"redstone_wire"); S(-5,0,1,"stone")
    # R in2 and Y/R in1
    S(-4,1,0,"repeater",facing="west",delay=rd); S(-4,0,0,"stone")
    S(-4,1,1,"repeater",facing="west",delay=1); S(-4,0,1,"stone")
    S(-3,1,1,"stone")
    S(-2,1,1,"repeater",facing="west",delay=1); S(-2,0,1,"stone")
    # W chain
    S(-8,1,-2,"redstone_wire"); S(-8,0,-2,"stone")
    S(-7,2,-2,"redstone_wire"); S(-7,1,-2,"glass")
    S(-6,2,-2,"redstone_wire"); S(-6,1,-2,"stone")
    for i,dl in enumerate(wd):
        x=-5+i; S(x,2,-2,"repeater",facing="west",delay=dl); S(x,1,-2,"stone")
    S(-2,2,-2,"stone")
    S(-2,2,-1,"repeater",facing="north",delay=wr); S(-2,1,-1,"stone")
    S(-2,2,0,"stone")
    return d
def build3(dk=2, dx=4, dline=(4,4,4,4), ys=4, wd=(4,4,4), wr=1, rd=4):
    d = build2(dk=dk, dx=dx, dline=dline, ys=ys, wd=wd, wr=wr, rd=rd)
    d.remove(-3,0,-2)
    d.set(-4,-1,-2,"observer",facing="down")
    d.set(-4,0,-2,"stone")
    return d
def fixinit(d):
    for p,(b,pr) in list(d.blocks.items()):
        if b=="redstone_wall_torch":
            pr["lit"] = "true" if p==(-2,-2,-2) else "false"
    for p in [(-2,-2,-1),(-3,-2,0),(-3,0,-1),(-4,0,-1)] + [(x,-2,-2) for x in range(-12,-3)]:
        if p in d.blocks and d.blocks[p][0]=="repeater": d.blocks[p][1]["powered"]="true"
    return d
def build4(**kw):
    d = build3(**kw)
    R = d.remove; S = d.set
    for p in [(-5,1,1),(-4,1,1),(-3,1,1),(-2,1,1),(-5,0,1),(-4,0,1),(-3,0,1),(-2,0,1),
              (-8,1,-2),(-8,0,-2),(-7,2,-2),(-7,1,-2),(-2,2,-1),(-2,1,-1),(-2,2,0)]:
        R(*p)
    # Y + R in1 on z=-1
    S(-2,1,-1,"repeater",facing="west",delay=1)
    S(-3,1,-1,"stone")
    S(-3,2,-1,"redstone_wire"); S(-4,2,-1,"redstone_wire"); S(-4,1,-1,"stone")
    S(-5,2,-1,"redstone_wire"); S(-5,1,-1,"stone")
    S(-6,2,-1,"redstone_wire"); S(-6,1,-1,"stone")
    # W output path
    S(-2,2,-1,"stone"); S(-2,3,-2,"redstone_wire"); S(-2,3,-1,"redstone_wire")
    S(-2,2,0,"stone"); S(-2,3,0,"redstone_wire")
    return d
def build5(**kw):
    d = build4(**kw); d.set(-3,3,-1,"stone"); return d
def labcycle(d, n=4, show=False):
    lab = Lab(d, walls=True); lab.rest()
    out=[]
    for k in range(n):
        lab.flip(-1,-3,-2); t0=lab.t; ok=lab.rest(300)
        out.append((lab.doorway(), lab.t-t0-20, ok))
    print(out, lab.entity)
    return lab
def build6():
    d = build5(dline=(4,4,4))      # 3 reps out at x=-4..-6, U-turn at x=-7
    S = d.set; R = d.remove
    # 4th delay rep on the return path
    S(-6,-2,0,"repeater",facing="west",delay=4,powered="true")
    # right side redesign
    for p in list(d.blocks):
        if p[0]>=4 or p[0]==5: R(*p)
    R(3,3,-2)
    S(2,4,0,"sticky_piston",facing="down"); S(4,1,0,"sticky_piston",facing="west"); S(2,-2,0,"sticky_piston",facing="up")
    S(2,4,-1,"repeater",facing="north")
    S(2,-2,-1,"repeater",facing="north"); S(2,-3,-1,"stone")
    S(4,-2,-2,"stone"); S(4,-1,-2,"redstone_torch",lit="true"); S(4,0,-2,"stone")
    S(4,1,-2,"redstone_torch",lit="false"); S(4,1,-1,"repeater",facing="north"); S(4,0,-1,"stone")
    S(4,2,-2,"stone"); S(4,3,-2,"redstone_wire"); S(3,4,-2,"redstone_wire"); S(3,3,-2,"stone")
    return d
def build7():
    d = fixinit(build6())
    d.blocks[(-6,-2,0)][1]["powered"]="true"
    S=d.set; R=d.remove
    for p in list(d.blocks):
        if p[0]==-7: R(*p)
    # line: A(-4) B(-5) at z=-2 ; U-turn at x=-6 with rep C in it ; D' return ; D block
    S(-6,-2,-2,"redstone_wire"); S(-6,-3,-2,"stone")
    S(-6,-2,-1,"repeater",facing="north",delay=4,powered="true"); S(-6,-3,-1,"stone")
    S(-6,-2,0,"redstone_wire"); S(-6,-3,0,"stone")
    S(-5,-2,0,"repeater",facing="west",delay=4,powered="true"); S(-5,-3,0,"stone")
    S(-4,-2,0,"stone"); R(-4,-3,0)
    S(-4,-1,0,"redstone_wire")
    R(-5,-1,-1); R(-5,-2,-1)
    S(-4,0,-1,"redstone_wire"); S(-4,-1,-1,"stone")
    S(-4,0,0,"glass")
    # Ysig reroute
    S(-6,1,-2,"glass"); S(-6,1,-1,"redstone_wire"); S(-6,0,-1,"stone")
    R(-6,2,-1)
    S(-6,1,0,"redstone_wire"); S(-6,0,0,"stone")
    return d
