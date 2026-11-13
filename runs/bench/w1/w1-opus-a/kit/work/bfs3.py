import itertools
# cells: column x=1 y=-3..3 ; a=(0,-1)
# state: Bpos in {-2,-1}; B2ext bool (head at -2, requires Bpos==-1); stones dict pos->name ; Kext bool (head at a)
def step(st, op, mode):
    Bpos,B2ext,Kext,st_=st; s=dict(st_)
    occ=lambda p: p in s or p==(1,Bpos) or (B2ext and p==(1,-2)) or (Kext and p==(0,-1))
    def pushup(y0):
        # push chain in column 1 starting at y0 upward, only stones movable (and B if retracted)
        ys=[];y=y0
        while occ((1,y)):
            if (1,y) in s: ys.append(y)
            elif y==Bpos: ys.append('B')
            else: return None
            y+=1
        top=y
        if top>=2: return None  # would enter TM area
        return ys
    if op in ('Bl','Bh'):
        if (op=='Bl')!=(Bpos==-2): return st
        f=Bpos+1
        if occ((1,f)):
            ys=pushup(f)
            if ys is None: return None
            for y in reversed(ys): s[(1,y+1)]=s.pop((1,y))
            return (Bpos,B2ext,Kext,frozenset(s.items()))
        if (1,f+1) in s: s[(1,f)]=s.pop((1,f+1))
        return (Bpos,B2ext,Kext,frozenset(s.items()))
    if op=='B2p':
        if B2ext: return None
        if Bpos==-2:
            ys=pushup(-1)
            if ys is None: return None
            for y in reversed(ys): s[(1,y+1)]=s.pop((1,y))
            return (-1,False,Kext,frozenset(s.items()))
        # lo empty?
        if (1,-2) in s: return None
        if Bpos==-1: return (-2,False,Kext,frozenset(s.items()))
        if (1,-1) in s: s[(1,-2)]=s.pop((1,-1))
        return (Bpos,False,Kext,frozenset(s.items()))
    if op=='K':
        if mode=='open':  # retract: pull from b to a
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
closeds=[(-2,False,True,frozenset({(1,0):'S1',(1,1):'S2'}.items())),(-1,False,True,frozenset({(1,0):'S1',(1,1):'S2'}.items()))]
for n in range(1,11):
    found=[]
    for seq in itertools.product(['Bl','Bh','B2p','K'],repeat=n):
        if seq.count('K')!=1: continue
        for c in closeds:
            o=run(c,seq,'open')
            if o is None or not isopen(o): continue
            c2=run(o,seq,'close')
            if c2==c: found.append((seq,c[0]))
    if found:
        for f in found: print(n,f)
        break
