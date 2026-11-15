from lsim import *
import itertools,sys
def closed(w):
    ok=all(w.get((x,0))==('S',) for x in (0,1))
    return ok and all((x,0) not in w for x in (2,3))
def opened(w):
    return all((x,0) not in w for x in range(0,4)) and w.get((-1,0))==('S',)
base=[((-3,0),'E','P1'),((-2,0),'E','P2'),((-1,2),'S','V')]
stones=[(-1,0),(-1,1)]
cands=[]
for x in range(-5,2):
    for y in range(-2,4):
        for d in 'ENWS':
            cands.append(((x,y),d,'X'))
res=[]
for cx in cands:
    pos=[b[0] for b in base]+stones
    if cx[0] in pos: continue
    if cx[0][1]==0 and cx[0][0]>=0: continue
    for st in itertools.product([0,1],repeat=4):
        w={}
        for (p,d,n),s in zip(base+[cx],st): w[p]=('P',d,bool(s),n,False)
        for s in stones: w[s]=('S',)
        names=[b[2] for b in base]+['X']
        for o1 in itertools.permutations(names):
            w1=w
            for n in o1: w1=setp(w1,n,True)
            if not closed(w1): continue
            for o2 in itertools.permutations(names):
                w2=w1
                for n in o2: w2=setp(w2,n,False)
                if opened(w2): res.append((cx,st,o1,o2)); 
print(len(res))
for r in res[:40]: print(r)
