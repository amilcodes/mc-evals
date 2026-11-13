import itertools
import lane1d as L
from collections import deque
L.LO, L.HI = -6, 8
def ixp(x): return x - L.LO
def goal_open(st): return all(st[ixp(x)] is None for x in (0,1,2)) and st[ixp(-1)]=='S' and st[ixp(3)]=='S'
def goal_closed(st): return all(st[ixp(x)]=='S' for x in (0,1,2))
def bfs(start, goal, cap=60000):
    prev={start:None}; q=deque([start])
    while q:
        s=q.popleft()
        if goal(s):
            path=[]
            while prev[s] is not None:
                p,ps=prev[s]; path.append(p); s=ps
            return path[::-1]
        if len(prev)>cap: return 'cap'
        for p in L.pistons_at(s):
            t=L.pulse(s,p)
            if t is not None and t!=s and t not in prev:
                prev[t]=(p,s); q.append(t)
    return None
def mk(stones, pl):
    cells=[None]*(L.HI-L.LO+1)
    for x in stones: cells[ixp(x)]='S'
    for (x,d,sk) in pl: cells[ixp(x)]=('P',d,sk,False)
    return tuple(cells)
def cycle(start, cycles=4):
    s=start; out=[]
    for c in range(cycles):
        p1=bfs(s,goal_open)
        if p1 in (None,'cap'): return ('open fail',c,out)
        for p in p1: s=L.pulse(s,p)
        p2=bfs(s,goal_closed)
        if p2 in (None,'cap'): return ('close fail',c,out)
        for p in p2: s=L.pulse(s,p)
        out.append((len(p1),len(p2)))
    return out, s
best=None
results=[]
for npw in range(1,5):
  for pw in itertools.combinations([-2,-3,-4,-5,-6],npw):
    for npe in range(0,4):
      for pe in itertools.combinations([4,5,6,7],npe):
        for sx in [(),(-1,),(3,)]:
          if set(sx)&(set(pw)|set(pe)): continue
          st=mk([0,1,2]+list(sx), [(x,1,True) for x in pw]+[(x,-1,True) for x in pe])
          r=cycle(st,3)
          if isinstance(r[0],str): continue
          results.append((len(pw)+len(pe), pw, pe, sx, r[0]))
results.sort()
for r in results[:10]: print(r)
print("count", len(results))
