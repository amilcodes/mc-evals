import heapq, sys
import bfs4 as B
from bfs4 import *
pc = lambda m: bin(m).count('1')
def h_close(s): return pc(Dm & ~s[0]) + (0 if s[1]==0 else 1)
def search(start, goal, hfun, cap):
    cnt = 0
    pq = [(hfun(start), 0, cnt, start)]
    prev = {start: None}
    while pq:
        f, g, _, s = heapq.heappop(pq)
        if goal(s):
            path = []
            while prev[s] is not None:
                a, p = prev[s]; path.append(a); s = p
            return path[::-1], len(prev)
        if len(prev) > cap: return None, len(prev)
        for a, t in succ(s, list(range(len(PIST)))):
            if t not in prev:
                prev[t] = (a, s); cnt += 1
                heapq.heappush(pq, (g + 1 + 2 * hfun(t), g + 1, cnt, t))
    return None, len(prev)
if __name__ == "__main__":
    cap = int(sys.argv[1])
    path, n = search((Fm, 0, 0), closed_goal, h_close, cap)
    print("found" if path else "none", None if path is None else len(path), n, flush=True)
    if path:
        print([(a[0], PIST[a[1]][0]) for a in path])
