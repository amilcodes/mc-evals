X=2
def top_col():
    d = Design()
    for y in range(5): d.set(X,y,0,"stone")
    for y in (7,8,9,10): d.set(X,y,0,"sticky_piston",facing="down")
    lev = {}
    def src(name, by, z):   # block at (X,by,z), dust on top, lever block at (X-1,by+1,z)
        d.set(X,by,z,"stone"); d.set(X,by+1,z,"redstone_wire")
        d.set(X-1,by+1,z,"stone"); d.set(X-1,by+2,z,"lever",face="floor",facing="north")
        lev[name]=(X-1,by+2,z)
    # S5: dust on wall top
    d.set(X,6,-1,"redstone_wire"); d.set(X-1,6,-1,"stone"); d.set(X-1,7,-1,"lever",face="floor",facing="north"); lev["S5"]=(X-1,7,-1)
    src("S7",7,-1); src("S9",9,-1); src("S11",11,-1)
    src("S8",8,1); src("S10",10,1)
    d.set(X,6,2,"sticky_piston",facing="north"); d.set(X,6,3,"stone"); d.set(X,7,3,"lever",face="floor",facing="north"); lev["Q"]=(X,7,3)
    return d, lev

SYM = {"air":".", "stone":"#"}
def sym(s):
    if s in SYM: return SYM[s]
    if s.startswith("sticky_piston"): return "P" if "extended=true" in s else "p"
    if s.startswith("piston_head"): return "|"
    if s.startswith("moving"): return "m"
    return "?"
def col(lab, lo=-1, hi=11):
    return "".join(sym(lab.block(X,y,0)) for y in range(hi,lo-1,-1)) + "  st:" + sym(lab.block(X,6,1))

state = {}
def start():
    global lab, lev, state
    d, lev = top_col()
    lab = Lab(d, walls=True)
    state = {k: False for k in lev}
    print("lost", lab.lost); print("t=%d %s" % (lab.t, col(lab)))
def act(cmds, wait=6, show=True):
    """cmds like 'S8+ S7+' ; flips then steps wait ticks"""
    for c in cmds.split():
        name, on = c[:-1], c[-1]=="+"
        if state[name] != on:
            lab.flip(*lev[name]); state[name]=on
    lab.step(wait)
    if show: print("t=%d %-14s %s" % (lab.t, cmds, col(lab)))
