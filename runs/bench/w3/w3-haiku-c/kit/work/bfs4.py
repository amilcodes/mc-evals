# Full 5x5 region at z=0 (corners included). Pistons sit just outside the 5x5 at the end of every row/column.
from collections import deque
import sys
R = [(x, y) for x in range(-1, 4) for y in range(-1, 4)]
idx = {c: i for i, c in enumerate(R)}
D = [(x, y) for x in range(3) for y in range(3)]
F = [(-1, y) for y in range(3)] + [(3, y) for y in range(3)] + [(x, -1) for x in range(3)] + [(x, 3) for x in range(3)]
def bit(c): return 1 << idx[c]
def mask(cs):
    m = 0
    for c in cs: m |= bit(c)
    return m
Dm, Fm = mask(D), mask(F)
PIST = []
for y in range(-1, 4):
    PIST.append(((-2, y), (1, 0)))
    PIST.append(((4, y), (-1, 0)))
for x in range(-1, 4):
    PIST.append(((x, -2), (0, 1)))
    PIST.append(((x, 4), (0, -1)))

def inR(c): return c in idx

def chain_shift(S, start, d, s):
    dx, dy = d
    chain = []
    c = start
    while inR(c) and (S >> idx[c]) & 1:
        chain.append(c); c = (c[0] + dx, c[1] + dy)
    if not chain: return None
    if s > 0:
        end = c  # first cell after chain
        if not inR(end) or (S >> idx[end]) & 1: return None
    else:
        tgt = (chain[0][0] - dx, chain[0][1] - dy)
        if not inR(tgt) or (S >> idx[tgt]) & 1: return None
    sx, sy = dx * s, dy * s
    newS = S
    for c in chain: newS &= ~bit(c)
    for c in chain: newS |= bit((c[0] + sx, c[1] + sy))
    return newS

def succ(state, pist):
    S, HEAD, EXT = state
    out = []
    for i in pist:
        (px, py), (dx, dy) = PIST[i]
        h = (px + dx, py + dy); hb = bit(h) if inR(h) else 0
        d = (dx, dy)
        p2 = (px + 2 * dx, py + 2 * dy)
        if not (EXT >> i) & 1:
            if not ((S | HEAD) & hb):
                out.append((('ext', i), (S, HEAD | hb, EXT | (1 << i))))
            elif S & hb:
                nS = chain_shift(S, h, d, +1)
                if nS is not None:
                    out.append((('push', i), (nS, HEAD | hb, EXT | (1 << i))))
        else:
            H2 = HEAD & ~hb; E2 = EXT & ~(1 << i)
            if inR(p2) and (S >> idx[p2]) & 1:
                if inR(h) and not (S & hb) and not (HEAD & hb) or True:
                    nS = (S & ~bit(p2)) | hb
                    out.append((('pull', i), (nS, H2, E2)))
            else:
                out.append((('ret', i), (S, H2, E2)))
    return out

def bfs(start, goal, pist, maxn):
    prev = {start: None}
    q = deque([start])
    while q:
        s = q.popleft()
        if goal(s):
            path = []
            while prev[s] is not None:
                a, p = prev[s]; path.append(a); s = p
            return path[::-1], len(prev)
        if len(prev) > maxn: return None, len(prev)
        for a, t in succ(s, pist):
            if t not in prev:
                prev[t] = (a, s); q.append(t)
    return None, len(prev)

open_goal = lambda s: s[0] == Fm and s[1] == 0 and s[2] == 0
closed_goal = lambda s: (s[0] & Dm) == Dm and s[1] == 0 and s[2] == 0
if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
    pist = list(range(len(PIST)))
    path, n = bfs((Fm, 0, 0), closed_goal, pist, cap)
    print("open->closed", None if path is None else len(path), "explored", n, flush=True)
    if path:
        print([ (a[0], PIST[a[1]][0]) for a in path])
