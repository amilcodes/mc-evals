import random, sys
from grid2d import *
from collections import deque
random.seed(int(sys.argv[1]))
corner_out = [(-2,0,(1,0),True),(-2,2,(1,0),True),(4,0,(-1,0),True),(4,2,(-1,0),True),
              (0,-2,(0,1),True),(2,-2,(0,1),True),(0,4,(0,-1),True),(2,4,(0,-1),True)]
mid_frame = [(-1,1,(1,0),True),(3,1,(-1,0),True),(1,-1,(0,1),True),(1,3,(0,-1),True)]
mid_out = [(-2,1,(1,0),True),(4,1,(-1,0),True),(1,-2,(0,1),True),(1,4,(0,-1),True)]
extra_pos = [(-1,-1),(3,-1),(-1,3),(3,3),(-2,-1),(-2,3),(4,-1),(4,3),(-1,-2),(3,-2),(-1,4),(3,4),(-2,-2),(4,4),(-2,4),(4,-2),(0,-1),(0,3),(-1,0),(3,0),(-1,2),(3,2),(1,0),(1,2),(0,1),(2,1)]
dirs = [(1,0),(-1,0),(0,1),(0,-1)]
def explore(start, cap):
    seen = {start}; q = deque([start]); best = -1
    while q and len(seen) < cap:
        s = q.popleft()
        e = sum(1 for (x,y) in D if s[ix(x,y)]==0)
        if e > best: best = e
        if best == 9: return 9, len(seen)
        for p in pistons_now(s):
            t = pulse(s, p)
            if t is not None and t not in seen:
                seen.add(t); q.append(t)
    return best, len(seen)
base = mid_frame + mid_out + corner_out
results = []
for trial in range(int(sys.argv[2])):
    k = random.randint(1, 5)
    extra = []
    occupied = set((x,y) for x,y,_,_ in base)
    for pos in random.sample([p for p in extra_pos if p not in occupied], k):
        extra.append((pos[0], pos[1], random.choice(dirs), random.random()<0.6))
    # some extra stones (not in D)
    pist = base + extra
    taken = set((x,y) for x,y,_,_ in pist)
    ns = random.randint(0, 3)
    stones = list(D) + [c for c in [(-1,-1),(3,-1),(-1,3),(3,3)] if c not in taken][:ns]
    start = make(stones, pist)
    best, n = explore(start, 30000)
    if best == 9:
        print("FULL", trial, "extra", extra, "stones", stones, flush=True)
    results.append(best)
print("best per trial max", max(results), "hist", {b: results.count(b) for b in set(results)})
