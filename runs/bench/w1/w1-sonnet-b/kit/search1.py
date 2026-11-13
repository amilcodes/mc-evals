from sim import *
import sim, itertools
def mk(extra=None):
    st={}
    st[(-1,1)]=('s',);st[(-1,2)]=('s',);st[(-1,0)]=('s',)
    st[(-2,1)]=('p','X','E');st[(-3,1)]=('p','Y','E');st[(-1,3)]=('p','V','S')
    if extra: st.update(extra)
    return st
def search(st0,alpha,maxlen):
    k0=key(st0);found=[]
    for L in range(1,maxlen+1):
        for S in itertools.product(alpha,repeat=L):
            c=run(st0,S)
            if (0,1) in c and (1,1) in c and c[(0,1)][0]=='s' and c[(1,1)][0]=='s':
                if key(run(c,S))==k0:
                    found.append(S)
        if found: return found
    return found
if __name__=="__main__":
    st=mk()
    print(search(st,['X','Y','V'],10)[:20])
