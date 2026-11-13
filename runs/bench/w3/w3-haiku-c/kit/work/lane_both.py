import itertools, sys
from lane_ext import *
from lane_cycle import row
def goal_D_empty(st): return all(st[ix(x)]==0 for x in (0,1,2))
def goal_D_full(st): return all(st[ix(x)]==1 for x in (0,1,2))
found=0
W_sets = [(-2,-3,-4)]
for pw in [(-2,-3,-4),(-2,-3),(-2,-3,-4,-5)]:
  for pe in [(),(4,),(4,5),(4,5,6),(4,5,6,7)]:
    for sx in [(),(-1,),(4,)]:
      for sx2 in [(),(3,),(5,)]:
        pl = [(x,(1,0),True) for x in pw] + [(x,(-1,0),True) for x in pe]
        stones = [0,1,2] + list(sx) + list(sx2)
        if set(sx)&set(pw) or set(sx2)&set(pe) or set(sx)&set(pe) or set(sx2)&set(pw): continue
        start = mk(stones, pl)
        # closed start: D full. Find open (D empty, F west & east stones) then back to D full with pistons retracted
        p1 = bfs(start, lambda st: goal_D_empty(st) and st[ix(-1)]==1 and st[ix(3)]==1, 40000)
        if p1 in (None,'cap'): continue
        s = start
        for a in p1: s = E.act(s,a[0],a[1])
        p2 = bfs(s, goal_D_full, 40000)
        if p2 in (None,'cap'): continue
        t = s
        for a in p2: t = E.act(t,a[0],a[1])
        print("cycle candidate pw",pw,"pe",pe,"sx",sx,"sx2",sx2,"open-len",len(p1),"close-len",len(p2),
              "close==start", t==start, flush=True)
        found+=1
print("found", found)
