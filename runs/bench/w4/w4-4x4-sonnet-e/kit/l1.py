from lsim import *
import itertools
def mk(st1,st2,stv):
    return {(-3,0):('P','E',st1,'P1',False),(-2,0):('P','E',st2,'P2',False),(-1,0):('S',),(-1,1):('S',),(-1,2):('P','S',stv,'V',False)}
def closed(w): return all(w.get((x,0))==('S',) for x in (0,1))
def opened(w):
    return all((x,0) not in w for x in (0,1)) and w.get((-1,0))==('S',)
names=['P1','P2','V']
for st in itertools.product([0,1],repeat=3):
  for order in itertools.permutations(names):
    for grp in [0]:
      w=mk(*st)
      for n in order: w=setp(w,n,True)
      if not closed(w): continue
      for n in order: w=setp(w,n,False)
      if opened(w) and not any(b[0]=='H' for b in w.values()): print(st,order)
