import itertools,sys
exec(open('search.py').read().split("s0=")[0])
def run(state, seq):
    st=dict(state)
    for n in seq:
        st=pulse2(st,n)
        if st is None: return None
    return st
def stones(st): return {p for p,v in st.items() if v[1]=='stone'}
def isclosed(st):
    s=stones(st); return {(0,1),(1,1)}<=s and not any(p in s for p in [(-1,1),(-1,2)])
def isopen(st):
    s=stones(st); return {(-1,1),(-1,2)}<=s and not any(p[0]>=0 for p in s)
def search(s0,syms,maxL):
    for L in range(1,maxL+1):
        res=[]
        for T in itertools.product(syms,repeat=L):
            cur=s0; ok=True
            for k in range(4):
                cur=run(cur,T)
                if cur is None: ok=False;break
                if k%2==0 and not isclosed(cur): ok=False;break
                if k%2==1 and not isopen(cur): ok=False;break
            if ok: res.append(''.join(T))
        if res: return L,res[:20]
    return None
s0={(-4,1):('Q','sp','e'),(-3,1):('P','sp','e'),(-2,1):('B','sp','e'),(-1,1):('S','stone',None),(-1,2):('G','stone',None),(-1,3):('A','sp','d')}
print(search(s0,'QPBA',9))
