from sim import *
import itertools,sys
def pal(st0,alpha,maxhalf):
    k0=key(st0);res=[]
    for h in range(0,maxhalf+1):
        for mid in ([None]+list(alpha)):
            for Q in itertools.product(alpha,repeat=h):
                S=list(Q)+([mid] if mid else [])+list(reversed(Q))
                if not S: continue
                c=run(st0,S)
                if (0,1) in c and (1,1) in c and c[(0,1)][0]=='s' and c[(1,1)][0]=='s':
                    if key(run(c,S))==k0: res.append(''.join(S))
        if res: return res
    return res
layouts={}
def base():
    st={}
    st[(-1,1)]=('s',);st[(-1,2)]=('s',);st[(-1,0)]=('s',)
    return st
# layout A: X,Y row, V top
A=base();A[(-2,1)]=('p','X','E');A[(-3,1)]=('p','Y','E');A[(-1,3)]=('p','V','S')
layouts['A']=A
# layout B: add bottom V2
B=dict(A);B[(-1,-1)]=('p','W','N');layouts['B']=B
# layout C: add Z behind Y
C=dict(A);C[(-4,1)]=('p','Z','E');layouts['C']=C
# layout D: V2 at (-2,3)? stone parked at (-2,2)
D=dict(A);D[(-2,2)]=('s',);D[(-2,3)]=('p','U','S');layouts['D']=D
for n,st in layouts.items():
    alpha=sorted({b[1] for b in st.values() if b[0]=='p'})
    r=pal(st,alpha,7)
    print(n,alpha,r[:10],flush=True)
