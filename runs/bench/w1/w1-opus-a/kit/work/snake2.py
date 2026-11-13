import sys,time
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
DIRS=[(0,-1,0),(1,0,0),(-1,0,0),(0,1,0),(0,0,1),(0,0,-1)]
def tube(p):
    x,y,z=p
    if z==0: return -1<=x<=3 and -1<=y<=3
    if (x,y) in [(-1,-1),(-1,3),(3,-1),(3,3)]: return False
    return -1<=x<=3 and -1<=y<=3
# fixed blocks
B2=(-3,1,0); LO=(-2,1,0); CROSS=(-2,1,1); SUP=(-2,0,1); AUXB=(-2,2,1); AUXK=(-1,-1,1); K=(-1,-1,0)
SRC=(-3,3,0)  # level dust on top of first observer at (-3,2,0)
occupied={B2,LO,CROSS,SUP,AUXB,AUXK,K,SRC,(-3,4,1),(-3,3,1),(-2,4,1),(-2,3,1),(-1,4,1),(-1,3,1),(-1,4,0),(-2,4,0),(-2,3,0),(-1,3,0)}
XR=(-5,-1); YR=(-3,4); ZR=(-2,2)
def allowed(p):
    x,y,z=p
    if not (XR[0]<=x<=XR[1] and YR[0]<=y<=YR[1] and ZR[0]<=z<=ZR[1]): return False
    if tube(p) or p in occupied: return False
    return True
# tap: observer at p watching q emits into target cell t (t is B2, SUP, AUXB, K, AUXK)
TGT={'B2':{B2},'B':{SUP,AUXB},'K':{K,AUXK}}
sensitive={B2,LO,SUP,AUXB,K,AUXK,CROSS,(-3,1,1)}  # outputs must not hit these unless tap; (-3,1,1) solid would be bad but observer ok
def bad_out(o):
    if o in sensitive: return True
    if o in occupied: return True
    x,y,z=o
    # walls adjacent to hi' (-1,1,0): (-1,1,+-1) ; frame stones adjacent to pistons
    if o in [(-1,1,1),(-1,1,-1),(-1,0,0),(-1,2,0),(-1,1,0)]: return True
    return False
order=['B2','B','K','B2','B','K','B2','B']
res=[]
def lb(p,ti):
    # min steps to reach a feeder of order[ti]: feeder adjacent to target
    if ti>=len(order): return 0
    return max(0,min(sum(abs(a-b) for a,b in zip(p,t)) for t in TGT[order[ti]])-2)
MAXLEN=int(sys.argv[1])
t0=time.time()
def dfs(path,ti,last):
    if res or time.time()-t0>150: return
    if ti==len(order): res.append(list(path)); return
    p=path[-1]
    if len(path)+lb(p,ti)+ (len(order)-ti-1)*2 > MAXLEN: return
    for d in DIRS:
        n=add(p,d)
        if n in path or not allowed(n): continue
        o=add(n,d)
        idx=len(path)
        if o in TGT[order[ti]] and idx-last>=2:
            path.append(n); dfs(path,ti+1,idx); path.pop()
        elif not bad_out(o) and not any(o in TGT[k] for k in TGT):
            path.append(n); dfs(path,ti,last); path.pop()
first=(-3,2,0)  # watches SRC (above), emits down into B2 -> tap B2 #1
dfs([SRC,first],1,1)
print(res, time.time()-t0)
