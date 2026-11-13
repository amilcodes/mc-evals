import sys
from grid2d import *
from collections import deque
def explore(start, cap=400000):
    seen = {start}; q = deque([start]); best = -1; bestst=None
    while q and len(seen) < cap:
        s = q.popleft()
        e = sum(1 for (x,y) in D if s[ix(x,y)]==0)
        if e > best: best = e; bestst = s
        for p in pistons_now(s):
            t = pulse(s, p)
            if t is not None and t not in seen:
                seen.add(t); q.append(t)
    return len(seen), best, bestst
# F-cells as inward sticky pistons; outer pullers at distance 2 facing inward
Fp = []
for y in range(3):
    Fp += [(-1,y,(1,0),True),(3,y,(-1,0),True)]
for x in range(3):
    Fp += [(x,-1,(0,1),True),(x,3,(0,-1),True)]
outer = []
for y in range(3):
    outer += [(-2,y,(1,0),True),(4,y,(-1,0),True)]
for x in range(3):
    outer += [(x,-2,(0,1),True),(x,4,(0,-1),True)]
stones = list(D)
start = make(stones, Fp + outer)
n, best, bs = explore(start)
print("states", n, "best empty D", best)
print(show(bs))
