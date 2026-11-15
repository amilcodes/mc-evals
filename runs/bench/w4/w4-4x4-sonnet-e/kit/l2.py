from lsim import *
import itertools
from l1 import mk,closed,opened,names
for st in itertools.product([0,1],repeat=3):
  for o1 in itertools.permutations(names):
    w=mk(*st)
    for n in o1: w=setp(w,n,True)
    if not closed(w): continue
    for o2 in itertools.permutations(names):
      w2=w
      for n in o2: w2=setp(w2,n,False)
      if opened(w2) and not any(b[0]=='H' for b in w2.values()): print(st,o1,o2)
