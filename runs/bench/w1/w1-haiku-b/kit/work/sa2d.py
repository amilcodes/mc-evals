import random, sys, itertools, time
from sim2d import DOOR, RING, DIRS, flip_orders, _BOX
import sim2d

def check(pist, spares, box):
    sim2d._BOX[0] = box
    bodies = [p[0] for p in pist]
    if len(set(bodies)) != len(bodies): return -1, None
    if any(c in DOOR or c in RING for c in bodies): return -1, None
    sp = set(spares)
    if len(sp) != len(spares) or sp & set(bodies) or sp & DOOR: return -1, None
    n = len(pist)
    ef0 = tuple(p[3]=='B' for p in pist)
    heads0 = {(p[0][0]+DIRS[p[1]][0], p[0][1]+DIRS[p[1]][1]) for j,p in enumerate(pist) if ef0[j]}
    if heads0 & (DOOR|sp|set(bodies)): return -1, None
    S0 = (frozenset(DOOR | sp), ef0)
    best = -1; found=None
    for perm, S1 in flip_orders(S0, pist, list(range(n))):
        st = S1[0]
        sc = (9 - len(DOOR & st)) + len(RING & st)
        if sc <= best: continue
        # check return
        back = False
        for perm2, S2 in flip_orders(S1, pist, list(range(n))):
            if S2 == S0: back=True; break
        if back:
            best = sc; found=(perm, perm2 if False else None, S1)
            if sc == 21: break
        else:
            best = max(best, sc*0 + sc - 100)  # penalize non-returning
            best = max(best, sc - 100)
    if found is None:
        return best, None
    return best, found

def rand_cell(box):
    (x0,x1),(y0,y1)=box
    return (random.randint(x0,x1), random.randint(y0,y1))

def allowed_cells(box):
    (x0,x1),(y0,y1)=box
    return [(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1) if (x,y) not in DOOR and (x,y) not in RING]

def run(seed, box, K, iters, spare_n=3):
    random.seed(seed)
    cells = allowed_cells(box)
    pist = [(random.choice(cells), random.choice('nsew'), random.random()<0.5, random.choice('AB')) for _ in range(K)]
    spares = random.sample([c for c in cells], spare_n)
    cur, _ = check(pist, spares, box)
    best_overall = (cur, pist, spares)
    T = 1.0
    for it in range(iters):
        p2 = list(pist); s2 = list(spares)
        r = random.random()
        if r < 0.4:
            i = random.randrange(K); c,d,st,t = p2[i]
            p2[i] = (random.choice(cells) if random.random()<0.5 else c, random.choice('nsew') if random.random()<0.5 else d, (not st) if random.random()<0.3 else st, ('B' if t=='A' else 'A') if random.random()<0.3 else t)
        elif r < 0.7:
            i = random.randrange(K); c,d,st,t = p2[i]
            p2[i] = (random.choice(cells), d, st, t)
        else:
            i = random.randrange(spare_n); s2[i] = random.choice(cells)
        v, info = check(p2, s2, box)
        if v >= cur or random.random() < 2.718 ** ((v-cur)/max(T,1e-3)):
            pist, spares, cur = p2, s2, v
            if cur > best_overall[0]:
                best_overall = (cur, list(pist), list(spares))
        T = max(0.05, T*0.9995)
        if cur == 21 and info is not None:
            break
    return best_overall

if __name__ == "__main__":
    seed = int(sys.argv[1]); K=int(sys.argv[2]); iters=int(sys.argv[3])
    box = ((-2,3),(-2,3))
    t0=time.time()
    b = run(seed, box, K, iters)
    print(seed, K, b[0], b[1], b[2], round(time.time()-t0,1))
