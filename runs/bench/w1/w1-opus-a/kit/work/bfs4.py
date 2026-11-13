import itertools,sys
# like bfs3 but in close mode, pushes reaching y>=2 are blocked (no-op); in open invalid
BLOCK='block'
def step(st, op, mode):
    Bpos,B2ext,Kext,st_=st; s=dict(st_)
    occ=lambda p: p in s or p==(1,Bpos) or (B2ext and p==(1,-2)) or (Kext and p==(0,-1))
    def pushup(y0):
        ys=[];y=y0
        while occ((1,y)):
            if (1,y) in s: ys.append(y)
            elif y==Bpos: ys.append(y)
            else: return BLOCK
            y+=1
        if y>=2: return BLOCK if mode=='close' else None
        return ys
    def mv(ys):
        nonlocal Bpos
        for y in reversed(ys):
            if y==Bpos and (1,y) not in s: Bpos=y+1
            else: s[(1,y+1)]=s.pop((1,y))
    if op in ('Bl','Bh','B'):
        if op=='Bl' and Bpos!=-2: return st
        if op=='Bh' and Bpos!=-1: return st
        f=Bpos+1
        if occ((1,f)):
            ys=pushup(f)
            if ys is None: return None
            if ys==BLOCK: return st
            mv(ys); return (Bpos,B2ext,Kext,frozenset(s.items()))
        if (1,f+1) in s: s[(1,f)]=s.pop((1,f+1))
        return (Bpos,B2ext,Kext,frozenset(s.items()))
    if op=='B2p':
        if (1,-2) in s: return None
        if Bpos==-2:
            ys=pushup(-2)
            if ys is None: return None
            if ys==BLOCK: return st
            mv(ys); return (Bpos,False,Kext,frozenset(s.items()))
        if Bpos==-1: return (-2,False,Kext,frozenset(s.items()))
        if (1,-1) in s: s[(1,-2)]=s.pop((1,-1))
        return (Bpos,False,Kext,frozenset(s.items()))
    if op=='K':
        if mode=='open':
            if not Kext: return None
            if (1,-1) in s: s[(0,-1)]=s.pop((1,-1))
            return (Bpos,B2ext,False,frozenset(s.items()))
        else:
            if Kext: return None
            if (0,-1) in s:
                if occ((1,-1)): return None
                s[(1,-1)]=s.pop((0,-1))
            return (Bpos,B2ext,True,frozenset(s.items()))
def run(st,seq,mode):
    for op in seq:
        st=step(st,op,mode)
        if st is None: return None
    return st
def isopen(st):
    Bpos,B2ext,Kext,s=st; s=dict(s)
    return Bpos==-2 and not B2ext and (1,-1) in s and (0,-1) in s and (1,0) not in s and (1,1) not in s
S=frozenset({(1,0):'S1',(1,1):'S2'}.items())
closeds=[(-2,False,True,S),(-1,False,True,S)]
alph=sys.argv[1].split(',')
for n in range(1,12):
    found=[]
    for seq in itertools.product(alph,repeat=n):
        if seq.count('K')!=1: continue
        for c in closeds:
            o=run(c,seq,'open')
            if o is None or not isopen(o): continue
            c2=run(o,seq,'close')
            if c2==c: found.append((seq,c[0]))
    if found:
        for f in found[:20]: print(n,f)
        break
