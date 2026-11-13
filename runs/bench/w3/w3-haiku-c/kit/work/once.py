# Each piston performs exactly one stroke per flip (ext or ret, in any order). Search 1D row.
import itertools, sys
from collections import deque
import ext2 as E
import os
os.environ['BOX']='-6,8,1,1'
from lane_ext import ix, mk
def run_phase(start, goal_fn, pistons_list, cap=200000):
    # pistons_list: indices of pistons that must each act exactly once (their action is forced: toggle)
    idx_list = pistons_list
    n = len(idx_list); pos = {p:k for k,p in enumerate(idx_list)}
    start_state = (start, 0)
    prev = {start_state: None}; q = deque([start_state])
    while q:
        s, used = q.popleft()
        if used == (1<<n)-1 and goal_fn(s):
            path=[]; cur=(s,used)
            while prev[cur] is not None:
                a, pc = prev[cur]; path.append(a); cur = pc
            return path[::-1], s
        if len(prev) > cap: return 'cap', None
        for k,p in enumerate(idx_list):
            if used >> k & 1: continue
            c = s[p]
            if c < 2 or c >= 100: continue
            ext = E.pdec(c)[2]
            t = E.act(s, p, 'ret' if ext else 'ext')
            if t is None: continue
            ns = (t, used | (1<<k))
            if ns not in prev:
                prev[ns] = ((p, 'ret' if ext else 'ext'), (s, used)); q.append(ns)
    return None, None
def goal_open(s): return all(s[ix(x)]==0 for x in (0,1,2)) and s[ix(-1)]==1 and s[ix(3)]==1
if __name__ == "__main__":
    # opening: pistons at west, all direct (start retracted), stones 0,1,2
    for pw in [(-2,-3,-4),(-2,-3,-4,-5),(-2,-3,-4,-5,-6)]:
        for sx in [(),(-1,),(3,),(-1,3)]:
            st = mk([0,1,2]+list(sx), [(x,(1,0),True) for x in pw])
            pl = [ix(x) for x in pw]
            path, end = run_phase(st, goal_open, pl)
            print(pw, sx, 'open once-each:', None if path is None else (path if path=='cap' else len(path)), flush=True)
