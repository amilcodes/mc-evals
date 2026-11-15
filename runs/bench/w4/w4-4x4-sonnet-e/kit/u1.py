from sim import *
import itertools,sys
slots={
 'L2':((-2,0),'E'),'L3':((-3,0),'E'),'L4':((-4,0),'E'),'L5':((-5,0),'E'),
 'Vu':((-1,2),'S'),'Vd':((-1,-2),'N'),'Wu':((-2,2),'S'),'Wd':((-2,-2),'N'),
}
parked={'Vu':(-1,1),'Vd':(-1,-1),'Wu':(-2,1),'Wd':(-2,-1)}
def closed(w): return all(w.get((x,0))==('S',) for x in (0,1)) and all(w.get((x,0)) is None for x in (2,3))
found=0
names=list(slots)
for r in range(3,7):
  for sub in itertools.combinations(names,r):
    if not any(n.startswith('L') for n in sub): continue
    # line pistons must be contiguous from L2? allow any
    for stonesel in itertools.product([0,1],repeat=3):
        stones=[(-1,0)]
        if stonesel[0]: stones.append((-2,0))
        if stonesel[1]: stones.append((-3,0))
        for n in sub:
            if n in parked: stones.append(parked[n])
        if len(set(stones))!=len(stones): continue
        occupied=[slots[n][0] for n in sub]
        if any(s in occupied for s in stones): continue
        w0={}
        for n in sub: w0[slots[n][0]]=('P',slots[n][1],n)
        for s in stones: w0[s]=('S',)
        # extra stonesel[2]: parked stones for non-present V? skip
        for perm in itertools.permutations(sub):
            w1=run(w0,perm)
            if not closed(w1): continue
            if run(w1,perm)==w0:
                print(sub,stones,perm); found+=1
                if found>20: sys.exit()
print('done',found)
