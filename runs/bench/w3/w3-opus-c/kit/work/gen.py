import sys
sys.setrecursionlimit(10000)
from pdbuild import Design

DIRS = {(1,0,0):"east",(-1,0,0):"west",(0,1,0):"up",(0,-1,0):"down",(0,0,1):"south",(0,0,-1):"north"}
def add(a,b): return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
def sub(a,b): return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def nbrs(c): return [add(c,d) for d in DIRS]
def manh(a,b): return sum(abs(a[i]-b[i]) for i in range(3))

def is_wall(c):
    x,y,z=c
    if z==0: return False
    return ((x in(-1,3)) and 0<=y<=2) or ((y in(-1,3)) and 0<=x<=2)
def is_hall(c):
    x,y,z=c
    return 0<=x<=2 and 0<=y<=2

class Builder:
    def __init__(self):
        self.d = Design("open")
        self.used = set()
        self.reserved = set()   # cells that must stay air / not be used by chains
        self.qc = set()
        self.pistons = set()
        self.fronts = set()
    def put(self, c, block, **p):
        assert c not in self.used, ("dup", c, block)
        assert not is_wall(c) and not (is_hall(c) and c[2]!=0), ("wall/hall", c)
        self.d.set(*c, block, **p); self.used.add(c)
        if block in ("piston","sticky_piston"):
            self.pistons.add(c); self.qc.add(add(c,(0,1,0)))
    def obs(self, c, watch):
        f = DIRS[sub(watch,c)]
        self.put(c, "observer", facing=f)
        self.fronts.add(watch)
        return add(c, sub(c,watch))  # back cell

    def free(self, c, bounds):
        (x0,x1),(y0,y1),(z0,z1) = bounds
        x,y,z=c
        if not (x0<=x<=x1 and y0<=y<=y1 and z0<=z<=z1): return False
        if c in self.used or c in self.reserved or is_wall(c) or is_hall(c): return False
        if c in self.fronts: return False
        return True

    def route(self, src, dst_prev, dst, n, bounds, allowed_back=()):
        """chain of observers: path[0] watches src, ..., last observer at dst watching dst_prev.
        total observers n (including dst). path[-2] must be dst_prev (if n>=2)."""
        best=[None]
        target_len = n
        def back_ok(cell, prev, nxt, path_set):
            b = add(cell, sub(cell, prev))
            if b in self.qc: return False
            if nxt is not None and b == nxt: return True
            if b in path_set: return True
            if b in allowed_back: return True
            if b in self.qc: return False
            if b in self.used: return False
            if b in self.reserved: return False
            return True
        path=[]
        pset=set()
        def dfs(cur, prev, k):
            # cur placed as path[k-1]; need total target_len; last must be dst
            if k == target_len:
                return cur == dst
            rem = target_len - k
            for d in sorted(DIRS, key=lambda d: manh(add(cur,d), dst)):
                nx = add(cur,d)
                if nx in pset: continue
                last = (k+1 == target_len)
                if last:
                    if nx != dst: continue
                    if cur != dst_prev: continue
                else:
                    if nx == dst: continue
                    if not self.free(nx, bounds): continue
                    if manh(nx, dst_prev) > rem - 2: continue
                    if manh(nx, dst_prev) % 2 != (rem-2) % 2: continue
                # check back of cur (cur watches prev, back = cur + (cur-prev)) with nxt = nx
                if not back_ok(cur, prev, nx, pset): continue
                path.append(nx); pset.add(nx)
                if dfs(nx, cur, k+1): return True
                path.pop(); pset.discard(nx)
            return False
        # first observer
        for d in sorted(DIRS, key=lambda d: manh(add(src,d), dst)):
            c0 = add(src,d)
            if c0 != dst and not self.free(c0,bounds): continue
            if n == 1:
                if c0 == dst: 
                    return [c0]
                continue
            if c0 == dst: continue
            if manh(c0,dst_prev) > n-2 or manh(c0,dst_prev)%2 != (n-2)%2: continue
            path[:] = [c0]; pset.clear(); pset.add(c0)
            if dfs(c0, src, 1):
                return list(path)
        return None

    def place_chain(self, src, path, final_back_ok=True):
        prev = src
        for c in path:
            self.obs(c, prev)
            prev = c

from collections import deque
def _route2(self, src, dst_prev, dst, n, bounds, allowed_back=()):
    """BFS shortest path then pad with detours to exact n observers."""
    # BFS from src's neighbors to dst_prev
    start_cands = [add(src,d) for d in DIRS]
    prev = {}
    q = deque()
    for c in start_cands:
        if c == dst_prev or self.free(c,bounds):
            if c == dst: continue
            prev[c] = src; q.append(c)
    found = False
    while q:
        c = q.popleft()
        if c == dst_prev: found=True; break
        for d in DIRS:
            nx = add(c,d)
            if nx in prev or nx == dst: continue
            if nx != dst_prev and not self.free(nx,bounds): continue
            prev[nx]=c; q.append(nx)
    if not found: return None
    path=[dst_prev]
    while prev[path[-1]] != src: path.append(prev[path[-1]])
    path.reverse(); path.append(dst)
    def backs_ok(path):
        ps=set(path)
        full=[src]+path
        for i in range(1,len(full)-1):
            c=full[i]; b=add(c,sub(c,full[i-1]))
            nxt = full[i+1]
            if b in self.qc: return False
            if b == nxt or b in ps: continue
            if b in allowed_back: continue
            if b in self.used or b in self.reserved: return False
            if b == src: continue
        return True
    import itertools
    # pad
    tries=0
    while len(path) < n:
        need = n-len(path)
        if need % 2: return None
        ps=set(path)
        done=False
        full=[src]+path
        cand=[]
        for i in range(0,len(full)-2):  # segment full[i]->full[i+1], don't touch last segment into dst
            a,b2=full[i],full[i+1]
            if i==0: continue
            dvec=sub(b2,a)
            for e in DIRS:
                if e==dvec or e==(-dvec[0],-dvec[1],-dvec[2]): continue
                a2,b3=add(a,e),add(b2,e)
                if a2 in ps or b3 in ps or a2==src or b3==src: continue
                if not self.free(a2,bounds) or not self.free(b3,bounds): continue
                cand.append((i,a2,b3))
        for (i,a2,b3) in cand:
            # full index i is a; insert after path index i-1
            newp = path[:i]+[a2,b3]+path[i:]
            if backs_ok(newp) or len(newp)<n:
                path=newp; done=True; break
        if not done: return None
    if len(path)!=n or not backs_ok(path): return None
    return path
Builder.route = _route2

def _route3(self, src, dst_prev, dst, n, bounds, allowed_back=()):
    def safe_back(c, p):
        b = add(c, sub(c, p))
        if b in self.qc: return False
        if b == dst: return True
        if b in allowed_back: return True
        if b in self.used:
            g=self.d.get(*b)
            if g and g[0] in ("observer","glass"): return True
            if g and g[0]=="repeater":
                fd={"north":(0,0,-1),"south":(0,0,1),"east":(1,0,0),"west":(-1,0,0)}[g[1]["facing"]]
                dv=sub(b,c)
                if fd[0]*dv[0]+fd[1]*dv[1]+fd[2]*dv[2]==0: return True
            return False
        if b in self.reserved and b not in getattr(self,'soft',()): return False
        return True
    def okcell(c):
        return c == dst_prev or (self.free(c,bounds) and c != dst)
    prev = {}
    q = deque()
    for d in DIRS:
        c = add(src,d)
        if okcell(c) and safe_back(c, src):
            prev[c]=src; q.append(c)
    found=False
    while q:
        c=q.popleft()
        if c==dst_prev: found=True; break
        for d in DIRS:
            nx=add(c,d)
            if nx in prev or nx==src: continue
            if not okcell(nx): continue
            if not safe_back(nx, c): continue
            prev[nx]=c; q.append(nx)
    if not found: return None
    path=[dst_prev]
    while prev[path[-1]] != src: path.append(prev[path[-1]])
    path.reverse()
    # dst_prev back must be dst or safe: already ensured by safe_back
    def valid(path):
        full=[src]+path
        if len(set(path))!=len(path): return False
        for i in range(1,len(full)):
            if not safe_back(full[i], full[i-1]): return False
            if full[i]!=dst_prev and not self.free(full[i],bounds): return False
        return full[-1]==dst_prev
    while len(path)+1 < n:
        if (n - len(path) - 1) % 2: return None
        full=[src]+path
        ps=set(path)
        done=False
        for i in range(1,len(full)-1):
            a,b2=full[i],full[i+1]
            dvec=sub(b2,a)
            for e in DIRS:
                if e==dvec or e==(-dvec[0],-dvec[1],-dvec[2]): continue
                a2,b3=add(a,e),add(b2,e)
                if a2 in ps or b3 in ps or a2==src or b3==src or a2==dst or b3==dst: continue
                newp = path[:i]+[a2,b3]+path[i:]
                if valid(newp):
                    path=newp; done=True; break
            if done: break
        if not done: return None
    if len(path)+1 != n: return None
    return path+[dst]
Builder.route = _route3

import random as _random
def _route4(self, src, dst_prev, dst, n, bounds, allowed_back=(), budget=400000):
    if not self.free(dst_prev, bounds) or dst in self.used: return None
    p = _route3(self, src, dst_prev, dst, n, bounds, allowed_back)
    if p: return p
    def safe_back(c, pr):
        b = add(c, sub(c, pr))
        if b in self.qc: return False
        if b == dst: return True
        if b in self.used:
            g=self.d.get(*b)
            if g and g[0] in ("observer","glass"): return True
            if g and g[0]=="repeater":
                fd={"north":(0,0,-1),"south":(0,0,1),"east":(1,0,0),"west":(-1,0,0)}[g[1]["facing"]]
                dv=sub(b,c)
                if fd[0]*dv[0]+fd[1]*dv[1]+fd[2]*dv[2]==0: return True
            return False
        if b in self.reserved and b not in getattr(self,'soft',()): return False
        return True
    def okcell(c):
        return c == dst_prev or (self.free(c,bounds) and c != dst)
    # BFS distance to dst_prev over ok cells
    dist={dst_prev:0}; q=deque([dst_prev])
    while q:
        c=q.popleft()
        for d in DIRS:
            nx=add(c,d)
            if nx in dist or not okcell(nx): continue
            dist[nx]=dist[c]+1; q.append(nx)
    steps = n-1  # cells before dst: path[0..n-2], path[n-2]==dst_prev
    path=[]; pset=set(); cnt=[0]
    rnd=_random.Random(hash((src,dst,n)))
    def dfs(cur, pr):
        cnt[0]+=1
        if cnt[0]>budget: return False
        k=len(path)  # cur is path[k-1]
        if k==steps:
            return cur==dst_prev and safe_back(cur,pr)
        if cur==dst_prev: return False
        rem=steps-k
        ds=list(DIRS); rnd.shuffle(ds)
        for d in ds:
            nx=add(cur,d)
            if nx in pset or nx==src or nx not in dist: continue
            if dist[nx]>rem-1 or (dist[nx]-(rem-1))%2: continue
            # back of cur given next nx
            b=add(cur,sub(cur,pr))
            if b in self.qc: continue
            if not (b==nx or safe_back(cur,pr)): continue
            path.append(nx); pset.add(nx)
            if dfs(nx,cur): return True
            path.pop(); pset.discard(nx)
        return False
    for d in DIRS:
        c0=add(src,d)
        if c0 not in dist: continue
        if dist[c0]>steps-1 or (dist[c0]-(steps-1))%2: continue
        path[:]=[c0]; pset.clear(); pset.add(c0)
        if dfs(c0,src):
            full=list(path)
            # final check of dst_prev back
            return full+[dst]
    return None
Builder.route = _route4
