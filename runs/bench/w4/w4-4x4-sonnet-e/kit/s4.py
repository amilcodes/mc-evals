from sim import *
import itertools,sys
base=[((-3,0),'E','P1'),((-2,0),'E','P2'),((-1,2),'S','V')]
stones=[(-1,0),(-1,1)]
def closed(w): return all(w.get((x,0))==('S',) for x in (0,1)) and all(w.get((x,0)) is None for x in (2,3))
cands=[]
for x in range(-5,2):
    for y in range(-2,4):
        for d in 'ENWS':
            cands.append(((x,y),d,'X'))
found=0
for cx in cands:
    pos=[b[0] for b in base]+stones
    if cx[0] in pos: continue
    if cx[0][1]==0 and cx[0][0]>=0: continue
    w0={}
    for (p,d,n) in base+[cx]: w0[p]=('P',d,n)
    for s in stones: w0[s]=('S',)
    names=['P1','P2','V','X']
    for n in range(1,8):
        for seq in itertools.product(names,repeat=n):
            if 'X' not in seq: continue
            w1=run(w0,seq)
            if not closed(w1): continue
            if run(w1,seq)==w0:
                print(cx,n,seq); found+=1; break
        if found>20: break
    if found>20: break
print('done',found)
