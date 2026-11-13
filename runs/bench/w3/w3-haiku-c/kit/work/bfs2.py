from collections import deque
import sys

def inreg(c):
    x, y = c
    if not (-1 <= x <= 3 and -1 <= y <= 3): return False
    if x in (-1, 3) and y in (-1, 3): return False
    return True

cells = [(x, y) for x in range(-1, 4) for y in range(-1, 4) if inreg((x, y))]
idx = {c: i for i, c in enumerate(cells)}
D = [(x, y) for x in range(3) for y in range(3)]
F = [(-1, y) for y in range(3)] + [(3, y) for y in range(3)] + [(x, -1) for x in range(3)] + [(x, 3) for x in range(3)]
def bit(c): return 1 << idx[c]
def mask(cs):
    m = 0
    for c in cs: m |= bit(c)
    return m
Dm, Fm = mask(D), mask(F)

PIST = []
for y in range(3):
    PIST.append(((-2, y), (1, 0)))
    PIST.append(((4, y), (-1, 0)))
for x in range(3):
    PIST.append(((x, -2), (0, 1)))
    PIST.append(((x, 4), (0, -1)))
NP = len(PIST)

def chain_shift(S, start, d, s):
    dx, dy = d
    chain = []
    c = start
    while c in idx and (S >> idx[c]) & 1:
        chain.append(c)
        c = (c[0] + dx, c[1] + dy)
    if not chain: return None
    sx, sy = dx * s, dy * s
    if s > 0:
        end = (chain[-1][0] + dx, chain[-1][1] + dy)
        if end not in idx or (S >> idx[end]) & 1: return None
    else:
        tgt = (chain[0][0] + sx, chain[0][1] + sy)
        if tgt not in idx or (S >> idx[tgt]) & 1: return None
    newS = S
    for c in chain: newS &= ~bit(c)
    for c in chain: newS |= bit((c[0] + sx, c[1] + sy))
    return newS

def succ(state):
    S, HEAD, EXT = state
    out = []
    for i, ((px, py), (dx, dy)) in enumerate(PIST):
        h = (px + dx, py + dy); hb = bit(h); d = (dx, dy)
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
            if p2 in idx and (S >> idx[p2]) & 1:
                nS = chain_shift(S, p2, d, -1)
                if nS is not None:
                    out.append((('pull', i), (nS, H2, E2)))
                # sticky pull always happens; if it fails (blocked), it is invalid
            else:
                out.append((('ret', i), (S, H2, E2)))
    return out

def bfs(start, goal, maxn=3_000_000):
    prev = {start: None}
    q = deque([start])
    while q:
        s = q.popleft()
        if goal(s):
            path = []
            while prev[s] is not None:
                a, p = prev[s]
                path.append(a); s = p
            return path[::-1], len(prev)
        if len(prev) > maxn: return None, len(prev)
        for a, t in succ(s):
            if t not in prev:
                prev[t] = (a, s)
                q.append(t)
    return None, len(prev)

if __name__ == "__main__":
    start_open = (Fm, 0, 0)
    closed_goal = lambda s: (s[0] & Dm) == Dm and s[1] == 0 and s[2] == 0
    open_goal = lambda s: s[0] == Fm and s[1] == 0 and s[2] == 0
    path, n = bfs(start_open, closed_goal)
    print("open->closed", None if path is None else len(path), "explored", n)
    if path: print(path)
    path2, n2 = bfs((Dm | (1 << idx[(-1,0)]) | (1 << idx[(3,0)]) | (1<<idx[(0,-1)]), 0, 0), open_goal)
    print("closed->open", None if path2 is None else len(path2), "explored", n2)
    if path2: print(path2)
