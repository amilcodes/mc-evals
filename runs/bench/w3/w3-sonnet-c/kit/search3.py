import itertools
exec(open('search.py').read().split("s0=")[0])
def short(st,n): return pulse2(st,n)
def long_(st,n):
    pos=[p for p,v in st.items() if v[0]==n][0]
    d=D[st[pos][2]]
    head=(pos[0]+d[0],pos[1]+d[1])
    nb=st
    if head in st:
        nb=push_chain(st,head,d)
        if nb is None: return None
        # head now at head cell; block at head+1 pulled back
        far=(head[0]+d[0],head[1]+d[1])
        if far in nb:
            nb=dict(nb); v=nb.pop(far); nb[head]=v
        return nb
    else:
        far=(head[0]+d[0],head[1]+d[1])
        if far in st:
            nb=dict(st); v=nb.pop(far); nb[head]=v; return nb
        return st
ACT={}
for n in 'PBA':
    ACT['s'+n]=(short,n); ACT['l'+n]=(long_,n)
def run(state,seq):
    st=dict(state)
    for a in seq:
        f,n=ACT[a]; st=f(st,n)
        if st is None: return None
    return st
def stones(st): return {p for p,v in st.items() if v[1]=='stone'}
def isclosed(st):
    s=stones(st); return {(0,1),(1,1)}<=s and not any(p in s for p in [(-1,1),(-1,2),(-1,0)])
def isopen(st):
    s=stones(st); return {(-1,1)}<=s and not any(p[0]>=0 for p in s)
s0={(-3,1):('P','sp','e'),(-2,1):('B','sp','e'),(-1,1):('S','stone',None),(-1,0):('G','stone',None),(-1,-1):('A','sp','u')}
import sys
names=list(ACT)
for L in range(1,9):
    res=[]
    for T in itertools.product(names,repeat=L):
        cur=s0; ok=True
        for k in range(4):
            cur=run(cur,T)
            if cur is None: ok=False;break
            if k%2==0 and not isclosed(cur): ok=False;break
            if k%2==1 and not isopen(cur): ok=False;break
        if ok: res.append(T)
    print(L,len(res),res[:5]); sys.stdout.flush()
    if res: break
