# abstract model: column x=1, row y=-1. pulse-driven sticky pistons B (movable, facing up), B2 at (1,-3) up, K at (-1,-1) east
import itertools
UP=(0,1); EAST=(1,0)
def add(p,d): return (p[0]+d[0],p[1]+d[1])
def apply(state, op, mode):
    # state: dict pos->name ; 'B' piston facing up; stones 'S1','S2'; static blocks
    s=dict(state)
    if op=='B':
        bp=[p for p,v in s.items() if v=='B'][0]; d=UP
    elif op=='B2':
        bp=(1,-3); d=UP
    elif op=='K':
        bp=(-1,-1); d=EAST
    f=add(bp,d)
    if f in s:
        # push chain
        chain=[];p=f
        while p in s:
            if s[p] in ('WALL','T'): return None
            chain.append(p); p=add(p,d)
        if len(chain)>12: return None
        # forbidden destination
        dest=p
        if mode=='close' and dest==(1,2): return None
        if dest[1]>=2 and dest[0]==1: return None
        if dest==(1,0) and False: pass
        for q in reversed(chain):
            s[add(q,d)]=s.pop(q)
        return s
    else:
        g=add(f,d)
        if g in s and s[g] not in ('WALL','T','static'):
            s[f]=s.pop(g)
        return s
def run(state, seq, mode):
    for op in seq:
        state=apply(state,op,mode)
        if state is None: return None
    return state
def norm(s): return tuple(sorted(s.items()))
static={(2,-1):'static'}
closedA={**static,(1,-2):'B',(1,0):'S1',(1,1):'S2'}
closedB={**static,(1,-1):'B',(1,0):'S1',(1,1):'S2'}
openS=lambda s: s.get((1,0)) is None and s.get((1,1)) is None and s.get((1,-1),'').startswith('S') and s.get((0,-1),'').startswith('S')
def isclosed(s): return s.get((1,0),'').startswith('S') and s.get((1,1),'').startswith('S')
res=[]
for n in range(1,10):
    for seq in itertools.product(['B','B2','K'],repeat=n):
        for c in (closedA,closedB):
            o=run(c,seq,'open')
            if o is None or not openS(o): continue
            c2=run(o,seq,'close')
            if c2 is None or norm(c2)!=norm(c): continue
            res.append((n,seq,'A' if c is closedA else 'B'))
    if res: break
for r in res: print(r)
