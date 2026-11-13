# BFS over piston toggle sequences (pistons can be pulsed any number of times, any order).
from collections import deque
DOOR = {(x,y) for x in range(3) for y in range(3)}
RING = {(x,-1) for x in range(3)} | {(x,3) for x in range(3)} | {(-1,y) for y in range(3)} | {(3,y) for y in range(3)}
DIRS = {'n':(0,-1),'s':(0,1),'e':(1,0),'w':(-1,0)}

def make_env(box):
    (x0,x1),(y0,y1) = box
    def inb(c): return x0<=c[0]<=x1 and y0<=c[1]<=y1
    return inb

def toggle(stones, ef, pist, i, inb):
    cell, d, sticky = pist[i]
    dx,dy = DIRS[d]
    F = (cell[0]+dx, cell[1]+dy); B = (cell[0]+2*dx, cell[1]+2*dy)
    bodies = {p[0] for p in pist}
    heads = {(p[0][0]+DIRS[p[1]][0], p[0][1]+DIRS[p[1]][1]) for j,p in enumerate(pist) if ef[j]}
    if not ef[i]:
        # extend
        if F in stones:
            chain=[]; c=F
            while c in stones:
                chain.append(c); c=(c[0]+dx,c[1]+dy)
                if len(chain)>12: return None
            if not inb(c) or c in bodies or c in heads: return None
            ns=set(stones)
            for q in chain: ns.discard(q)
            for q in chain: ns.add((q[0]+dx,q[1]+dy))
        else:
            if F in bodies or F in heads: return None
            ns=set(stones)
        nef=list(ef); nef[i]=True
        return frozenset(ns), tuple(nef)
    else:
        ns=set(stones)
        if sticky and B in ns:
            ns.discard(B); ns.add(F)
        nef=list(ef); nef[i]=False
        return frozenset(ns), tuple(nef)

def bfs(start, goal, pist, inb, limit=200000):
    seen = {start: None}
    q = deque([start]); n=0
    while q:
        s = q.popleft(); n+=1
        if goal(s): 
            # reconstruct
            path=[]; c=s
            while seen[c] is not None:
                p,i = seen[c]; path.append(i); c=p
            return list(reversed(path)), n
        if n>limit: return None, n
        for i in range(len(pist)):
            r = toggle(s[0], s[1], pist, i, inb)
            if r is None or r in seen: continue
            seen[r]=(s,i); q.append(r)
    return None, n

def layout_ok(pist, spares, box, limit=200000):
    inb = make_env(box)
    ef0 = tuple(False for _ in pist)
    S0 = (frozenset(DOOR|set(spares)), ef0)
    openg = lambda s: not (DOOR & s[0]) and RING <= s[0]
    p1, n1 = bfs(S0, openg, pist, inb, limit)
    if p1 is None: return None, n1
    # open state
    s=S0
    for i in p1: s = toggle(s[0], s[1], pist, i, inb)
    closedg = lambda t: t == S0 or (DOOR <= t[0] and t[1]==ef0)
    p2, n2 = bfs(s, closedg, pist, inb, limit)
    return (p1, p2), n1+n2

if __name__=="__main__":
    box=((-2,3),(-2,3))
    pist=[((0,-2),'s',True),((1,-2),'s',True),((2,-2),'s',True)]
    spares=[(-1,-1),(3,-1),(-2,0)]
    print(layout_ok(pist, spares, box))
