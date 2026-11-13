import itertools, sys
from search1d import ext, ret, run_order, LO, HI, RING

def occupied_ok(stones, pist, ef):
    heads = {pist[i][0]+pist[i][1] for i in range(len(pist)) if ef[i]}
    pos = {q[0] for q in pist}
    if heads & stones: return False
    if heads & pos: return False
    if any(h in (0,1,2) for h in heads) and False: return False
    return True

def search(max_piston=2, max_extra=4):
    cells_p = list(range(-7, -1)) + list(range(4, 8))   # outside doorway and ring? includes -2 and 4
    cells_p = [c for c in cells_p if c not in (-1,3)]
    pchoices = [(p, d, st) for p in cells_p for d in (-1, 1) for st in (False, True)]
    found = []
    for n in range(1, max_piston+1):
        for pset in itertools.combinations(pchoices, n):
            ppos = [q[0] for q in pset]
            if len(set(ppos)) < n: continue
            free = [x for x in range(LO, HI+1) if x not in ppos and x not in (0,1,2)]
            for ef0 in itertools.product([False, True], repeat=n):
                for T in itertools.product([False, True], repeat=n):
                    if not any(T): continue
                    ef1 = tuple((ef0[i] != T[i]) for i in range(n))
                    # open state must have heads outside ring
                    if any(ef1[i] and (pset[i][0]+pset[i][1]) in RING for i in range(n)): continue
                    if any(ef0[i] and (pset[i][0]+pset[i][1]) in RING for i in range(n)): continue
                    changing = [i for i in range(n) if T[i]]
                    for k in range(0, max_extra+1):
                        for extra in itertools.combinations(free, k):
                            S0 = frozenset((0,1,2) + extra)
                            if not occupied_ok(S0, list(pset), ef0): continue
                            if any(x in ppos for x in S0): continue
                            for oe in itertools.permutations(changing):
                                r = run_order(S0, list(pset), ef0, oe, None) if False else None
                                st, ef = S0, ef0
                                good = True
                                for i in oe:
                                    rr = ext(st, list(pset), ef, i) if not ef[i] else ret(st, list(pset), ef, i)
                                    if rr is None: good = False; break
                                    st, ef = rr
                                if not good or ef != ef1: continue
                                if any(x in st for x in (0,1,2)): continue
                                if not ({-1,3} <= st): continue
                                if not occupied_ok(st, list(pset), ef1): continue
                                # back
                                okb = False
                                for ob in itertools.permutations(changing):
                                    s2, e2 = st, ef1; g2 = True
                                    for i in ob:
                                        rr = ext(s2, list(pset), e2, i) if not e2[i] else ret(s2, list(pset), e2, i)
                                        if rr is None: g2 = False; break
                                        s2, e2 = rr
                                    if g2 and s2 == S0 and e2 == ef0:
                                        okb = True; break
                                if okb:
                                    found.append((pset, ef0, T, sorted(S0), oe, sorted(st)))
                                    break
    return found

if __name__ == "__main__":
    res = search(int(sys.argv[1]), int(sys.argv[2]))
    print(len(res))
    for r in res[:30]: print(r)
