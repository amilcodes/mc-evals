import sys
from bfs4 import *
import astar
corners = [(-1,-1),(3,-1),(-1,3),(3,3)]
start_open = (Fm | mask(corners), 0, 0)
def h_close(s): return pc(Dm & ~s[0]) + (0 if s[1]==0 else 1)
pc = lambda m: bin(m).count('1')
goal = lambda s: (s[0] & Dm) == Dm and s[1]==0 and s[2]==0
cap = int(sys.argv[1])
path, n = astar.search(start_open, goal, h_close, cap)
print("found" if path else "none", None if path is None else len(path), n, flush=True)
if path: print([(a[0], PIST[a[1]][0]) for a in path])
