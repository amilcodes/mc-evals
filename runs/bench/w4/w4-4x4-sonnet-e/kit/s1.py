from sim import *
import itertools
w0={(-3,0):('P','E','P1'),(-2,0):('P','E','P2'),(-1,0):('S',),(-1,1):('S',),(-1,2):('P','S','V')}
pist=['P1','P2','V']
def closed(w): return all(w.get((x,0))==('S',) for x in (0,1))
def opened(w): return all((x,0) not in w for x in (0,1)) and w.get((-1,0))==('S',)
for n in range(1,10):
    found=0
    for seq in itertools.product(pist,repeat=n):
        w1=run(w0,seq)
        if not closed(w1): continue
        w2=run(w1,seq)
        if opened(w2): print(n,seq); found+=1
        if found>5: break
    if found: break
