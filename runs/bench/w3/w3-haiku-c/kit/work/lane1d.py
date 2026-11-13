# 1D lane model (row y=1). Cells x in [LO..HI]. Contents: None (empty), 'S' stone, ('P', d, sticky, ext)
# Piston pulse semantics (one full extend+retract, the redstone short pulse):
#  - head cell p+d empty: sticky -> pulls block at p+2d into p+d (if movable); normal -> nothing
#  - head cell occupied by run R from p+d (k blocks): extend pushes run by +d (needs free cell after run)
#    then retract: sticky pulls back first block (net: tail shifts), normal: net push.
from collections import deque
LO, HI = -7, 3
def movable(c): return c == 'S' or (isinstance(c, tuple) and c[0] == 'P' and not c[3])

def pulse(state, p):
    cells = list(state)
    def get(x):
        return cells[x - LO] if LO <= x <= HI else 'WALL'
    def setc(x, v):
        cells[x - LO] = v
    blk = cells[p - LO]
    _, d, sticky, _ = blk
    h = p + d
    out = []
    if get(h) is None:
        if sticky:
            tgt = p + 2 * d
            b = get(tgt)
            if b is not None and b != 'WALL' and movable(b):
                setc(tgt, None); setc(h, b)
        return tuple(cells)
    if get(h) == 'WALL' or not movable(get(h)):
        return None
    # run from h
    run = []
    x = h
    while get(x) not in (None, 'WALL') and movable(get(x)):
        run.append(x); x += d
    end = x
    if get(end) != None:
        return None
    # push run by +d
    vals = [get(r) for r in run]
    for r in run: setc(r, None)
    for r, v in zip(run, vals): setc(r + d, v)
    if sticky:
        # retract: pull block at p+2d (first run element, now at h+d) back into h
        tgt = p + 2 * d
        b = get(tgt)
        if b is not None and movable(b):
            setc(tgt, None); setc(h, b)
    return tuple(cells)

def pistons_at(state):
    return [LO + i for i, c in enumerate(state) if isinstance(c, tuple)]

def goal_open(state):
    return state[0 - LO] is None and state[1 - LO] is None and state[2 - LO] is None and state[-1 - LO] == 'S' \
        and not isinstance(state[-1 - LO], tuple)

def bfs(start, goal, maxn=200000):
    prev = {start: None}
    q = deque([start])
    while q:
        s = q.popleft()
        if goal(s):
            path = []
            while prev[s] is not None:
                a, ps = prev[s]; path.append(a); s = ps
            return path[::-1]
        if len(prev) > maxn: return 'cap'
        for p in pistons_at(s):
            t = pulse(s, p)
            if t is not None and t not in prev:
                prev[t] = ((p), s); q.append(t)
    return None

def make(pistons, stones):
    cells = [None] * (HI - LO + 1)
    for x in stones: cells[x - LO] = 'S'
    for (x, d, sticky) in pistons: cells[x - LO] = ('P', d, sticky, False)
    return tuple(cells)

if __name__ == "__main__":
    import itertools
    res = []
    for k in range(1, 4):
        for pos in itertools.combinations(range(-6, -1), k):
            for stick in [True]:
                pist = [(x, +1, True) for x in pos]
                st = make(pist, [0, 1])
                path = bfs(st, goal_open)
                if path and path != 'cap':
                    print("FOUND", pos, path)
                    res.append((pos, path))
                    break
    print("done", len(res))
