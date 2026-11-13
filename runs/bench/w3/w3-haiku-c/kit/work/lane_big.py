import itertools
from lane_ext import *
def goal_D_empty(st): return all(st[ix(x)]==0 for x in (0,1,2))
found=0; tried=0
for npw in range(1,5):
  for pw in itertools.combinations([-2,-3,-4,-5,-6], npw):
    for nsx in range(0,4):
      for sx in itertools.combinations([-1,-2,-3,-4,-5,-6], nsx):
        if set(pw)&set(sx): continue
        for pe_on in [False]:
          st = mk([0,1,2]+list(sx), [(x,(1,0),True) for x in pw])
          tried+=1
          p = bfs(st, goal_D_empty, 40000)
          if p and p!='cap':
              found+=1
              print("D-empty FOUND west pist", pw, "extra", sx, "len", len(p), flush=True)
              if found>=3: raise SystemExit
print("tried", tried, "found", found)
