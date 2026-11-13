from grid2d import *
corner_out = [(-2,0,(1,0),True),(-2,2,(1,0),True),(4,0,(-1,0),True),(4,2,(-1,0),True),
              (0,-2,(0,1),True),(2,-2,(0,1),True),(0,4,(0,-1),True),(2,4,(0,-1),True)]
mid_frame = [(-1,1,(1,0),True),(3,1,(-1,0),True),(1,-1,(0,1),True),(1,3,(0,-1),True)]
stones = list(D) + [(-1,-1),(3,-1),(-1,3)]
start = make(stones, mid_frame + corner_out)
# BFS over all reachable states (bounded) and record max number of empty D cells
from collections import deque
seen = {start}; q = deque([start]); best = 0; bestst=None
while q and len(seen) < 300000:
    s = q.popleft()
    e = sum(1 for (x,y) in D if s[ix(x,y)]==0)
    if e > best: best = e; bestst = s
    for p in pistons_now(s):
        t = pulse(s, p)
        if t is not None and t not in seen:
            seen.add(t); q.append(t)
print("states", len(seen), "max empty D", best)
print(show(bestst))
