import itertools,sys
exec(open('work/bfs4.py').read().split("def run")[0])
_old=step
def step2(st,op,mode):
    if op=='Kp':
        Bpos,B2ext,Kext,st_=st; s=dict(st_)
        occb = (1,-1) in s or Bpos==-1
        if (0,-1) in s:
            if occb: return st  # chain into d (static) blocked
            s[(1,-1)]=s.pop((0,-1)); return (Bpos,B2ext,Kext,frozenset(s.items()))
        if (1,-1) in s: s[(0,-1)]=s.pop((1,-1))
        elif Bpos==-1: return None  # would fetch piston B into a - disallow
        return (Bpos,B2ext,Kext,frozenset(s.items()))
    return _old(st,op,mode)
def run(st,seq,mode):
    for op in seq:
        st=step2(st,op,mode)
        if st is None: return None
    return st
def isopen(st):
    Bpos,B2ext,Kext,s=st; s=dict(s)
    return Bpos==-2 and not B2ext and (1,-1) in s and (0,-1) in s and (1,0) not in s and (1,1) not in s
S=frozenset({(1,0):'S1',(1,1):'S2'}.items())
closeds=[(-2,False,False,S),(-1,False,False,S)]
alph=sys.argv[1].split(',')
for n in range(1,12):
    found=[]
    for seq in itertools.product(alph,repeat=n):
        for c in closeds:
            o=run(c,seq,'open')
            if o is None or not isopen(o): continue
            c2=run(o,seq,'close')
            if c2==c: found.append((seq,c[0]))
    if found:
        for f in found[:20]: print(n,f)
        break
    print('none',n,flush=True)
