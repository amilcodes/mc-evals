# 2D pulse model. Region: x in [X0..X1], y in [Y0..Y1] at z=0. Cell codes: 0 empty, 1 stone, 2+k piston kind k.
# kinds: index into DIRS x sticky: k = dir_index*2 + sticky
import heapq, itertools, sys
DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
import os
X0, X1, Y0, Y1 = [int(v) for v in os.environ.get('BOX', '-2,4,-2,4').split(',')]
W = X1 - X0 + 1; H = Y1 - Y0 + 1
def ix(x, y): return (y - Y0) * W + (x - X0)
def inside(x, y): return X0 <= x <= X1 and Y0 <= y <= Y1
D = [(x, y) for x in range(3) for y in range(3)]
F = [(-1, y) for y in range(3)] + [(3, y) for y in range(3)] + [(x, -1) for x in range(3)] + [(x, 3) for x in range(3)]
Dset = set(D); Fset = set(F)
def kind(d_index, sticky): return 2 + d_index * 2 + (1 if sticky else 0)
def decode(code):
    k = code - 2
    return DIRS[k // 2], bool(k % 2)

def pulse(st, p):
    """st: tuple. p: index. Returns new tuple or None."""
    code = st[p]
    d, sticky = decode(code)
    px, py = p % W + X0, p // W + Y0
    hx, hy = px + d[0], py + d[1]
    if not inside(hx, hy): return None
    h = ix(hx, hy)
    s = list(st)
    if st[h] == 0:
        if sticky:
            tx, ty = px + 2*d[0], py + 2*d[1]
            if inside(tx, ty):
                t = ix(tx, ty)
                if st[t] != 0:
                    s[h] = st[t]; s[t] = 0
                    return tuple(s)
                return None  # nothing to pull: no change -> treat as no-op
        return None  # no-op
    # run push
    run = []
    cx, cy = hx, hy
    while inside(cx, cy) and s[ix(cx, cy)] != 0:
        run.append(ix(cx, cy)); cx += d[0]; cy += d[1]
    if not inside(cx, cy): return None
    end = ix(cx, cy)
    if s[end] != 0: return None
    vals = [s[r] for r in run]
    for r in run: s[r] = 0
    for r, v in zip(run, vals):
        rx, ry = r % W + X0 + d[0], r // W + Y0 + d[1]
        s[ix(rx, ry)] = v
    if sticky:
        tx, ty = px + 2*d[0], py + 2*d[1]
        if inside(tx, ty):
            t = ix(tx, ty)
            if s[t] != 0:
                s[h] = s[t]; s[t] = 0
    return tuple(s)

def is_open(st):
    return all(st[ix(x,y)] == 0 for (x,y) in D) and all(st[ix(x,y)] == 1 for (x,y) in F)
def is_closed(st):
    return all(st[ix(x,y)] == 1 for (x,y) in D)
def hopen(st):
    return sum(1 for (x,y) in D if st[ix(x,y)] != 0) + sum(1 for (x,y) in F if st[ix(x,y)] != 1)
def hclose(st):
    return sum(1 for (x,y) in D if st[ix(x,y)] != 1)

def search(start, goal, h, cap=400000, pistons=None):
    if pistons is None:
        pistons = [i for i,c in enumerate(start) if c >= 2]
    start_g = 0
    prev = {start: None}
    pq = [(h(start), 0, 0, start)]
    cnt = 0
    while pq:
        f, g, _, s = heapq.heappop(pq)
        if goal(s):
            path = []
            while prev[s] is not None:
                a, ps = prev[s]; path.append((a, ps)); s = ps
            return path[::-1]
        if len(prev) > cap: return 'cap'
        for p in pistons_now(s):
            t = pulse(s, p)
            if t is not None and t not in prev:
                prev[t] = (p, s); cnt += 1
                heapq.heappush(pq, (g + 1 + 2*h(t), g + 1, cnt, t))
    return None

def pistons_now(s):
    return [i for i,c in enumerate(s) if c >= 2]

def show(st):
    rows = []
    for y in range(Y1, Y0-1, -1):
        row = ''
        for x in range(X0, X1+1):
            c = st[ix(x,y)]
            if c == 0: ch = '.'
            elif c == 1: ch = '#'
            else:
                d, sk = decode(c)
                ch = {(1,0):'>',(-1,0):'<',(0,1):'v',(0,-1):'^'}[d]
                ch = ch.upper() if sk else ch
            if (x,y) in D and c == 0: ch = '_'
            row += ch
        rows.append(f"{y:3d} {row}")
    return "\n".join(rows)

def make(stones, pistons):
    st = [0]*(W*H)
    for (x,y) in stones: st[ix(x,y)] = 1
    for (x,y,d,sk) in pistons:
        st[ix(x,y)] = kind(DIRS.index(d), sk)
    return tuple(st)
