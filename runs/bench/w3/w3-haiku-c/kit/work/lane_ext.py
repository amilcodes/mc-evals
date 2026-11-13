import os, itertools, sys
os.environ['BOX'] = '-6,8,1,1'
import ext2 as E
from collections import deque
# 1D row y=1, x in [-6..8]. D-cells: x=0,1,2. Goal: D empty, and F cells (-1,1),(3,1) stones.
Dl = [(0,1),(1,1),(2,1)]
def ix(x): return E.ix(x,1)
def succ(st):
    return E.succ(st)
def goal_open(st):
    return all(st[ix(x)] == 0 for (x,_,) in [(0,0),(1,0),(2,0)]) and st[ix(-1)] == 1 and st[ix(3)] == 1
def bfs(start, goal, cap=300000):
    prev = {start: None}; q = deque([start])
    while q:
        s = q.popleft()
        if goal(s):
            path=[]
            while prev[s] is not None:
                a, ps = prev[s]; path.append(a); s = ps
            return path[::-1]
        if len(prev) > cap: return 'cap'
        for a, t in succ(s):
            if t not in prev:
                prev[t] = (a, s); q.append(t)
    return None
def mk(stones, plist):
    st=[0]*(E.W*E.H)
    for x in stones: st[ix(x)] = 1
    for (x,d,sk) in plist: st[ix(x)] = E.pcode(E.DIRS.index(d), sk, False)
    return tuple(st)
if __name__ == "__main__":
    # try: west lane pistons at x<0 facing east; east lane pistons at x>2 facing west; extra stones anywhere outside D
    res=[]
    cand_w = [-2,-3,-4,-5]
    cand_e = [4,5,6,7]
    for nw in range(0,3):
     for nes in range(0,3):
      for pw in itertools.combinations(cand_w, nw):
       for pe in itertools.combinations(cand_e, nes):
        for ns in range(0,3):
         for sx in itertools.combinations([-1,-2,-3,-4,3,4,5], ns):
          plist=[(x,(1,0),True) for x in pw]+[(x,(-1,0),True) for x in pe]
          if set(pw)&set(sx) or set(pe)&set(sx): continue
          stones=[0,1,2]+list(sx)
          st=mk(stones, plist)
          path=bfs(st, goal_open, 60000)
          if path and path!='cap':
              print("FOUND west",pw,"east",pe,"extra",sx,"len",len(path), flush=True)
              res.append(path)
              if len(res)>=3: raise SystemExit
    print("searched; found", len(res))
