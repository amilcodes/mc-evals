def machine(d, px, sgn, rodlen, glue="slime_block"):
    """Pusher machine. px = x of the three pusher pistons at home. sgn=+1 pushes east, -1 pushes west.
    lanes: z=0 pushers, z=1 engine main, z=2 engine aux."""
    fwd = "east" if sgn>0 else "west"
    back = "west" if sgn>0 else "east"
    X = lambda k: px + sgn*k
    for y in (1,2,3):
        d.set(X(0),y,0,"sticky_piston",facing=fwd)
        d.set(X(0),y,1,glue)
        mat = "honey_block" if y!=2 else "slime_block"
        for k in range(1,rodlen+1):
            d.set(X(k),y,0,mat)
        d.set(X(rodlen+1),y,0,"stone")
    d.set(X(-1),1,0,"observer",facing=back)
    d.set(X(-1),3,0,"observer",facing=back)
    d.set(X(-1),2,0,glue)
    d.set(X(-1),2,1,glue)
    d.set(X(-1),2,2,"sticky_piston",facing=back)
    d.set(X(0),2,2,"observer",facing=fwd)
    # rear unit
    d.set(X(-2),2,1,"sticky_piston",facing=fwd)
    d.set(X(-3),2,1,"observer",facing=back)
    d.set(X(-2),2,2,glue)
    d.set(X(-3),2,2,glue)
    d.set(X(-4),2,2,"obsidian")
    return d

def Ltest():
    d = Design()
    machine(d,-8,1,1)
    for y in (1,2,3):
        for x in range(-5,0): d.set(x,y,0,"stone")
        d.set(5,y,0,"obsidian")
    # station A: levers directly? use stone blocks toggled: lever-powered pistons pushing stones
    for y in (1,3):
        d.set(-10,y,-2,"sticky_piston",facing="south"); d.set(-10,y,-1,"stone")
    d.set(-10,2,-2,"stone"); d.set(-11,2,-2,"lever",face="wall",facing="west")
    # station B: dust watched by O1 at (-11,2,1): cell (-12,2,1)
    d.set(-12,1,1,"stone"); d.set(-12,2,1,"redstone_wire")
    d.set(-13,1,1,"stone"); d.set(-13,2,1,"lever",face="floor",facing="north")
    return d
def show(ch, grep=None, lim=200):
    n=0
    for c in ch:
        s=f"{c[0]} {c[1]} {c[2]} -> {c[3]}"
        if grep and not any(g in s for g in grep): continue
        print(s); n+=1
        if n>=lim: break
