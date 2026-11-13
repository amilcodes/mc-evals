# 1D row search: door row y, cells x in [LO, HI]; pistons outside ring [-1,3]; all pistons share one signal.
import itertools, sys
LO, HI = -7, 7
RING = (-1, 3)

def ext(stones, pist, ext_flags, i):
    # pist: list of (pos, d, sticky); ext_flags: tuple of bools
    p, d, st = pist[i]
    f = p + d
    if ext_flags[i]:
        return None
    if f in stones:
        c = f
        chain = []
        while c in stones:
            chain.append(c); c += d
            if len(chain) > 12: return None
        if c < LO or c > HI: return None
        if any(q == c for q, _, _ in pist): return None
        if any(j != i and ext_flags[j] and pist[j][0] + pist[j][1] == c for j in range(len(pist))): return None
        new = set(stones)
        for x in chain: new.discard(x)
        for x in chain: new.add(x + d)
    else:
        if any(q == f for q, _, _ in pist): return None
        if any(j != i and ext_flags[j] and pist[j][0] + pist[j][1] == f for j in range(len(pist))): return None
        new = set(stones)
    ef = list(ext_flags); ef[i] = True
    return frozenset(new), tuple(ef)

def ret(stones, pist, ext_flags, i):
    p, d, st = pist[i]
    if not ext_flags[i]: return None
    new = set(stones)
    if st and (p + 2*d) in new:
        new.discard(p + 2*d); new.add(p + d)
    ef = list(ext_flags); ef[i] = False
    return frozenset(new), tuple(ef)

def run_order(stones, pist, ef, order, action):
    for i in order:
        r = ext(stones, pist, ef, i) if action == 'ext' else ret(stones, pist, ef, i)
        if r is None: return None
        stones, ef = r
    return stones, ef

def search(max_piston=2, max_extra=5):
    cells_p = list(range(-7, -2)) + list(range(5, 8))
    pchoices = [(p, d, st) for p in cells_p for d in (-1, 1) for st in (False, True)]
    found = []
    for n in range(1, max_piston+1):
        for pset in itertools.combinations(pchoices, n):
            ppos = [q[0] for q in pset]
            if len(set(ppos)) < n: continue
            # open state: pistons extended; heads must be outside ring
            if any((q[0]+q[1]) in RING for q in pset): continue
            ef0 = tuple([False]*n)
            ef1 = tuple([True]*n)
            free = [x for x in range(LO, HI+1) if x not in ppos and x not in (0,1,2)]
            for k in range(0, max_extra+1):
                for extra in itertools.combinations(free, k):
                    S0 = frozenset((0,1,2) + extra)
                    if any(x in ppos for x in S0): continue
                    # heads of pistons retracted at closed so nothing else
                    # try every ordering of extension and retraction
                    for oe in itertools.permutations(range(n)):
                        r = run_order(S0, list(pset), ef0, oe, 'ext')
                        if r is None: continue
                        S1, ef = r
                        if ef != ef1: continue
                        if any(x in S1 for x in (0,1,2)): continue
                        if not ({-1, 3} <= S1): continue
                        # return
                        ok_back = False
                        for orr in itertools.permutations(range(n)):
                            r2 = run_order(S1, list(pset), ef1, orr, 'ret')
                            if r2 is None: continue
                            if r2[0] == S0 and r2[1] == ef0:
                                ok_back = True; break
                        if ok_back:
                            found.append((pset, sorted(S0), oe, sorted(S1)))
                            break
                    # keep going
    return found

if __name__ == "__main__":
    res = search(int(sys.argv[1]) if len(sys.argv) > 1 else 2, int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    print(len(res))
    for r in res[:40]: print(r)
