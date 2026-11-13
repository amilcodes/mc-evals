# Faithful-ish model: separate extend / retract actions. Pistons are movable when retracted.
# Cell codes: 0 empty, 1 stone, 100 head (immovable), 2+ piston code: 2 + dirIndex*4 + sticky*2 + ext
import heapq, os
DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
X0,X1,Y0,Y1 = [int(v) for v in os.environ.get('BOX','-3,5,-3,5').split(',')]
W = X1-X0+1; H = Y1-Y0+1
def ix(x,y): return (y-Y0)*W + (x-X0)
def inside(x,y): return X0<=x<=X1 and Y0<=y<=Y1
D = [(x,y) for x in range(3) for y in range(3)]
F = [(-1,y) for y in range(3)] + [(3,y) for y in range(3)] + [(x,-1) for x in range(3)] + [(x,3) for x in range(3)]
def pcode(di, sticky, ext): return 2 + di*4 + (2 if sticky else 0) + (1 if ext else 0)
def pdec(c):
    k = c-2; return DIRS[k//4], bool((k//2)%2), bool(k%2)
def movable(c): return c == 1 or (c >= 2 and c < 100 and not (c-2)%2)  # retracted pistons only
def pistons(st): return [i for i,c in enumerate(st) if 2 <= c < 100]
def pos(i): return (i % W + X0, i//W + Y0)

def act(st, i, kind):
    s = list(st)
    px,py = pos(i); c = st[i]
    d, sticky, ext = pdec(c)
    hx,hy = px+d[0], py+d[1]
    if not inside(hx,hy): return None
    h = ix(hx,hy)
    if kind == 'ext':
        if ext: return None
        if s[h] == 0:
            s[h] = 100
        elif movable(s[h]):
            run=[]; cx,cy=hx,hy
            while inside(cx,cy) and movable(s[ix(cx,cy)]):
                run.append(ix(cx,cy)); cx+=d[0]; cy+=d[1]
            if not inside(cx,cy) or s[ix(cx,cy)] != 0: return None
            vals=[s[r] for r in run]
            for r in run: s[r]=0
            for r,v in zip(run,vals):
                rx,ry = (r%W+X0+d[0]), (r//W+Y0+d[1]); s[ix(rx,ry)] = v
            s[h] = 100
        else:
            return None
        s[i] = pcode(DIRS.index(d), sticky, True)
        return tuple(s)
    else:  # retract
        if not ext: return None
        if s[h] != 100: return None
        s[h] = 0
        if sticky:
            tx,ty = px+2*d[0], py+2*d[1]
            if inside(tx,ty):
                t = ix(tx,ty)
                if movable(s[t]):
                    s[h] = s[t]; s[t] = 0
        s[i] = pcode(DIRS.index(d), sticky, False)
        return tuple(s)

def succ(st):
    out=[]
    for i in pistons(st):
        ext = pdec(st[i])[2]
        t = act(st, i, 'ret' if ext else 'ext')
        if t is not None and t != st: out.append(((i, 'ret' if ext else 'ext'), t))
    return out

def make(stones, plist):
    st=[0]*(W*H)
    for (x,y) in stones: st[ix(x,y)] = 1
    for (x,y,d,sk) in plist:
        st[ix(x,y)] = pcode(DIRS.index(d), sk, False)
    return tuple(st)

def show(st):
    rows=[]
    for y in range(Y1,Y0-1,-1):
        row=''
        for x in range(X0,X1+1):
            c=st[ix(x,y)]
            if c==0: ch='.' if (x,y) not in D else '_'
            elif c==1: ch='#'
            elif c==100: ch='h'
            else:
                d,sk,ex=pdec(c); ch={(1,0):'>',(-1,0):'<',(0,1):'v',(0,-1):'^'}[d]
                ch = ch.upper() if sk else ch
                if ex: ch = '*'
            row+=ch
        rows.append(f"{y:3d} {row}")
    return "\n".join(rows)

def astar(start, goal, h, cap):
    prev={start:None}; cnt=0
    pq=[(h(start),0,0,start)]
    while pq:
        f,g,_,s=heapq.heappop(pq)
        if goal(s):
            path=[]
            while prev[s] is not None:
                a,ps=prev[s]; path.append((a,ps)); s=ps
            return path[::-1]
        if len(prev)>cap: return 'cap'
        for a,t in succ(s):
            if t not in prev:
                prev[t]=(a,s); cnt+=1
                heapq.heappush(pq,(g+1+2*h(t),g+1,cnt,t))
    return None

def hD(st): return sum(1 for (x,y) in D if st[ix(x,y)]!=0)
def is_open(st): return all(st[ix(x,y)]==0 for (x,y) in D) and all(st[ix(x,y)]==1 for (x,y) in F)
def is_closed(st): return all(st[ix(x,y)]==1 for (x,y) in D)
