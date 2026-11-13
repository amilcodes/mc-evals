# 2D single-layer piston sim (z=0 plane). Door cells D, ring R (must be stone when open).
import itertools, random, sys
DOOR = {(x,y) for x in range(3) for y in range(3)}
RING = {(x,-1) for x in range(3)} | {(x,3) for x in range(3)} | {(-1,y) for y in range(3)} | {(3,y) for y in range(3)}
DIRS = {'n':(0,-1),'s':(0,1),'e':(1,0),'w':(-1,0)}

class Cfg:
    def __init__(self, pistons, spares, box):
        # pistons: list of (cell, dir, sticky, typ) typ 'A' ext when ON, 'B' ext when OFF
        self.pistons = pistons; self.spares = spares; self.box = box

def inbox(c, box):
    (x0,x1),(y0,y1) = box
    return x0 <= c[0] <= x1 and y0 <= c[1] <= y1

def do_ext(st, pist, i):
    stones, ef = st
    cell, d, sticky, typ = pist[i]
    dx, dy = DIRS[d]
    F = (cell[0]+dx, cell[1]+dy)
    heads = {(p[0][0]+DIRS[p[1]][0], p[0][1]+DIRS[p[1]][1]) for j,p in enumerate(pist) if ef[j]}
    bodies = {p[0] for p in pist}
    if F in stones:
        chain=[]; c=F
        while c in stones:
            chain.append(c); c=(c[0]+dx,c[1]+dy)
            if len(chain)>12: return None
        if c in bodies or c in heads or c not in BOX_CHECK(): return None
        ns = set(stones)
        for q in chain: ns.discard(q)
        for q in chain: ns.add((q[0]+dx,q[1]+dy))
    else:
        if F in bodies or F in heads: return None
        ns = set(stones)
    nef = list(ef); nef[i]=True
    return frozenset(ns), tuple(nef)

_BOX = [None]
def BOX_CHECK():
    class C:
        def __contains__(self, c): return inbox(c, _BOX[0])
    return C()

def do_ret(st, pist, i):
    stones, ef = st
    cell, d, sticky, typ = pist[i]
    dx, dy = DIRS[d]
    F = (cell[0]+dx, cell[1]+dy); B = (cell[0]+2*dx, cell[1]+2*dy)
    ns = set(stones)
    if sticky and B in ns:
        ns.discard(B); ns.add(F)
    nef = list(ef); nef[i]=False
    return frozenset(ns), tuple(nef)

def apply(st, pist, i):
    return do_ext(st, pist, i) if not st[1][i] else do_ret(st, pist, i)

def flip_orders(S, pist, changing, maxperm=5000):
    for perm in itertools.permutations(changing):
        cur = S; ok=True
        for i in perm:
            r = apply(cur, pist, i)
            if r is None: ok=False; break
            cur = r
        if ok: yield perm, cur

def evaluate(cfg, box):
    _BOX[0] = box
    pist = cfg.pistons
    n = len(pist)
    bodies = {p[0] for p in pist}
    spares = set(cfg.spares)
    if (spares & bodies) or (spares & DOOR) or (spares & RING) and False:
        return -1, None
    ef0 = tuple(p[3]=='B' for p in pist)   # closed: B extended
    S0 = (frozenset(DOOR | spares), ef0)
    # heads of B pistons must not be in doorway
    for j,p in enumerate(pist):
        if ef0[j]:
            h = (p[0][0]+DIRS[p[1]][0], p[0][1]+DIRS[p[1]][1])
            if h in DOOR or h in bodies or h in spares: return -1, None
    changeON = [j for j in range(n) if pist[j][3]=='A' or pist[j][3]=='B']  # all pistons differ on each flip
    # ON: A extends, B retracts. All pistons change on each flip.
    best = -1; bestinfo=None
    for perm, S1 in flip_orders(S0, pist, changeON):
        stones, ef = S1
        if any(c in stones for c in DOOR): 
            score = 9 - len(DOOR & stones)
        else: score = 9
        ringfull = len(RING & stones)
        sc = score + ringfull
        if sc > best:
            best = sc; bestinfo=(perm, S1)
    return best, bestinfo

if __name__=="__main__":
    print("module ok")
