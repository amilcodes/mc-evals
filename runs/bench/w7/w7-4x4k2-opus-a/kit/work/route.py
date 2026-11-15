from collections import deque
DIRS={(1,0,0):'east',(-1,0,0):'west',(0,1,0):'up',(0,-1,0):'down',(0,0,1):'south',(0,0,-1):'north'}
def add(a,b): return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
def sub(a,b): return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def is_wall_or_hall(c):
    x,y,z=c
    if z==0: return False
    if 0<=x<=3 and 0<=y<=3: return True
    if x in(-1,4) and 0<=y<=3: return True
    if y in(-1,4) and 0<=x<=3: return True
    return False
class Router:
    def __init__(s, d, box, forbid=()):
        s.d=d; s.box=box; s.forbid=set(forbid); s.reserved_air=set(); s.noback=set()
    def free(s,c):
        (x0,y0,z0),(x1,y1,z1)=s.box
        x,y,z=c
        if not(x0<=x<=x1 and y0<=y<=y1 and z0<=z<=z1): return False
        if is_wall_or_hall(c): return False
        if c in s.d.blocks or c in s.forbid: return False
        return True
    def back_ok(s,b):
        if b in s.reserved_air: return True
        blk=s.d.blocks.get(b)
        if blk is None: return not is_wall_or_hall(b) and b not in s.noback
        return blk[0]=='observer'
    def route(s, src, start_cells, goal, maxlen=40):
        """src: cell the first chain observer watches. chain cells from a start cell (adjacent to src)
        to goal (the cell that must hold last chain observer). returns path list."""
        # BFS states: (cell, prev)
        q=deque()
        seen={}
        for c in start_cells:
            if s.free(c) or c==goal:
                q.append((c,src,[c])); 
        best=None
        while q:
            c,p,path=q.popleft()
            key=(c,p)
            if key in seen: continue
            seen[key]=1
            if len(path)>maxlen: continue
            b=add(c,sub(c,p))
            if not s.back_ok(b):
                continue
            if c==goal: return path
            for dv in DIRS:
                n=add(c,dv)
                if n in path: continue
                if n!=goal and not s.free(n): continue
                if n==p: continue
                # n's back would be n+(n-c); checked when popped
                q.append((n,c,path+[n]))
        return None
    def place(s, src, path):
        prev=src
        for c in path:
            s.d.set(*c,"observer",facing=DIRS[sub(prev,c)])
            prev=c
        # reserve back cells as air
        prev=src
        for c in path:
            b=add(c,sub(c,prev))
            if b not in s.d.blocks: s.reserved_air.add(b)
            prev=c
