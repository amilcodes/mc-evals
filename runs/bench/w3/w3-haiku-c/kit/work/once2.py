import itertools, os
os.environ['BOX']='-6,8,1,1'
import ext2 as E
from lane_ext import ix
from once import run_phase
def build(stones, pist):
    st=[0]*(E.W*E.H)
    for x in stones: st[ix(x)]=1
    for (x, inv) in pist:
        if not inv:
            st[ix(x)] = E.pcode(0, True, False)
        else:
            st[ix(x)] = E.pcode(0, True, True); st[ix(x+1)] = 100
    return tuple(st)
def goal_open(s): return all(s[ix(x)]==0 for x in (0,1,2)) and s[ix(-1)]==1 and s[ix(3)]==1
def goal_closed(s): return all(s[ix(x)]==1 for x in (0,1,2))
found=[]
cands=[-2,-3,-4,-5]
for n in range(1,5):
  for pos in itertools.combinations(cands,n):
    for invs in itertools.product([False,True], repeat=n):
      for sx in [(),(-1,),(3,),(-1,3)]:
        pist=list(zip(pos,invs))
        if any(inv and (x+1) in sx for x,inv in pist): continue
        if any(inv and (x+1) in (0,1,2) for x,inv in pist): continue
        if any(x in sx for x in pos): continue
        st=build([0,1,2]+list(sx), pist)
        pl=[ix(x) for x,_ in pist]
        p1,end1=run_phase(st, goal_open, pl, cap=100000)
        if p1 is None or p1=='cap': continue
        # closing: each piston toggles once again
        p2,end2=run_phase(end1, goal_closed, pl, cap=100000)
        if p2 is None or p2=='cap': continue
        found.append((pist,sx,len(p1),len(p2), end2==st))
        print("cycle", pist, sx, len(p1), len(p2), "returns", end2==st, flush=True)
        if len(found)>=8: raise SystemExit
print("done", len(found))
