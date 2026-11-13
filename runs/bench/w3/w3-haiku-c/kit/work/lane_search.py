import itertools, random
from lane1d import *
found = []
cands_p = list(range(-7, -1))
cands_s = list(range(-7, 0))
random.seed(1)
tried = 0
for kp in range(1, 4):
    for pos in itertools.combinations(cands_p, kp):
        for ks in range(0, 3):
            for spos in itertools.combinations([c for c in cands_s if c not in pos], ks):
                pist = [(x, +1, True) for x in pos]
                st = make(pist, [0, 1] + list(spos))
                path = bfs(st, goal_open, maxn=50000)
                tried += 1
                if path and path != 'cap':
                    found.append((pos, spos, path))
                    print("FOUND pist", pos, "extra stones", spos, "len", len(path), path, flush=True)
                    if len(found) > 5: raise SystemExit
print("tried", tried, "found", len(found))
