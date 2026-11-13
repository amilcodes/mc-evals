import bfs2, itertools, sys
from bfs2 import *
allp = list(bfs2.PIST)
def run(sel, cap=400000):
    bfs2.PIST[:] = [allp[i] for i in sel]
    bfs2.NP = len(bfs2.PIST)
    st_open = (Fm, 0, 0)
    closed_goal = lambda s: (s[0] & Dm) == Dm and s[1] == 0 and s[2] == 0
    path, n = bfs(st_open, closed_goal, maxn=cap)
    return (None if path is None else len(path)), n
# piston indices: 0 W0,1 E0,2 W1,3 E1,4 W2,5 E2,6 N0,7 S0,8 N1,9 S1,10 N2,11 S2
tests = {
 "rows only": [0,1,2,3,4,5],
 "W and N/S": [0,2,4,6,7,8,9,10,11],
 "W0 E0 N0 S0 N1 S1 N2 S2": [0,1,6,7,8,9,10,11],
 "all": list(range(12)),
}
for k,v in tests.items():
    print(k, run(v), flush=True)
