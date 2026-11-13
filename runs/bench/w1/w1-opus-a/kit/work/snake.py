import sys
sys.setrecursionlimit(10000)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
DIRS=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
def tube(p):
    x,y,z=p
    if z==0: return -1<=x<=3 and -1<=y<=3
    if (x,y) in [(-1,-1),(-1,3),(3,-1),(3,3)]: return False
    return -1<=x<=3 and -1<=y<=3
occupied={(-3,1,0),(-2,1,0),(-2,1,-1),(-2,0,-1),(-3,1,1),(-2,2,-1),(-1,-1,-1),
          (-1,4,-1),(-1,3,-1),(-1,4,0),(-2,3,0)}
def allowed(p):
    x,y,z=p
    if not (-3<=x<=-1 and -3<=y<=4 and -1<=z<=1): return False
    if tube(p) or p in occupied: return False
    return True
taps={'B2':{(-3,0,0):(-3,-1,0),(-3,2,0):(-3,3,0),(-3,0,1):(-3,-1,1),(-3,2,1):(-3,3,1)},
      'B':{(-2,-1,-1):(-2,-2,-1),(-2,0,0):(-2,0,1),(-2,3,-1):(-2,4,-1),(-2,2,0):(-2,2,1)},
      'K':{(-2,-1,0):(-3,-1,0),(-2,-1,-1):(-3,-1,-1),(-1,-2,-1):(-1,-3,-1),(-1,-2,0):(-1,-3,0)}}
auxtargets={(-3,1,0),(-3,1,1),(-2,0,-1),(-2,2,-1),(-1,-1,0),(-1,-1,-1)}
order=['B2','B','K','B2','B','K','B2','B']
src=(-1,4,-1); start=(-2,4,-1)
best=[None]
MAXLEN=int(sys.argv[1]) if len(sys.argv)>1 else 22
def outcell(p,q): return add(p,sub(p,q))
def ok_out(c,path_set):
    # output of non-tap observer: must be air (not occupied/aux) or will be snake
    if c in auxtargets or c in occupied: return False
    if tube(c): return False
    return True
res=[]
def dfs(path,ti,last_tap):
    if len(res)>=5: return
    p=path[-1]; q=path[-2] if len(path)>1 else src
    if ti==len(order):
        res.append(list(path)); return
    if len(path)>=MAXLEN: return
    for d in DIRS:
        n=add(p,d)
        if n==q or n in path or not allowed(n): continue
        # n watches p ; n output = n + (n-p)
        o=add(n,d)
        tgt=order[ti]
        istap = (n in taps[tgt] and taps[tgt][n]==p and len(path)-1-last_tap>=1)
        # spacing: tap index difference >=2
        idx=len(path)
        if istap and idx-last_tap>=2:
            path.append(n); dfs(path,ti+1,idx); path.pop()
        if ok_out(o,set(path)):
            # also must not accidentally be a tap of a wrong target (would power target)
            path.append(n); dfs(path,ti,last_tap); path.pop()
# first observer: start watches src
o0=add(start,sub(start,src))
dfs([start],0,-2)
for r in res: print(len(r),r)
