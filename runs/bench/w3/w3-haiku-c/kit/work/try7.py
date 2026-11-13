import sys
from grid2d import *
from collections import deque
corner_out = [(-2,0,(1,0),True),(-2,2,(1,0),True),(4,0,(-1,0),True),(4,2,(-1,0),True),
              (0,-2,(0,1),True),(2,-2,(0,1),True),(0,4,(0,-1),True),(2,4,(0,-1),True)]
mid_frame = [(-1,1,(1,0),True),(3,1,(-1,0),True),(1,-1,(0,1),True),(1,3,(0,-1),True)]
mid_out = [(-2,1,(1,0),True),(4,1,(-1,0),True),(1,-2,(0,1),True),(1,4,(0,-1),True)]
def explore(start, cap):
    seen = {start}; q = deque([start]); best = -1; bestst=None
    while q and len(seen) < cap:
        s = q.popleft()
        e = sum(1 for (x,y) in D if s[ix(x,y)]==0)
        if e > best: best = e; bestst = s
        for p in pistons_now(s):
            t = pulse(s, p)
            if t is not None and t not in seen:
                seen.add(t); q.append(t)
    return len(seen), best, bestst, len(q)
stones = list(D) + [(-1,-1),(3,-1),(-1,3)]
for name, pl in [("V3 all", mid_frame+mid_out+corner_out)]:
    n,b,bs,rem = explore(make(stones, pl), 400000)
    print(name, "states", n, "best", b, "queue left", rem)
    print(show(bs))
