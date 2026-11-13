import sys
from lane_ext import *
def row(s): return ''.join(('.' if s[ix(x)]==0 else '#' if s[ix(x)]==1 else ('h' if s[ix(x)]==100 else ('P' if not E.pdec(s[ix(x)])[2] else 'p'))) for x in range(-6,9))
def goal_D_empty(st): return all(st[ix(x)]==0 for x in (0,1,2))
def goal_closed(st): return all(st[ix(x)]==1 for x in (0,1,2)) and all(st[ix(x)] in (0,1,) or E.pdec(st[ix(x)])[2]==False for x in range(-6,9) if 2<=st[ix(x)]<100)
start = mk([0,1,2], [(-2,(1,0),True),(-3,(1,0),True),(-4,(1,0),True)])
p_open = bfs(start, goal_D_empty, 40000)
s = start
for a in p_open: s = E.act(s, a[0], a[1])
print("open state", row(s))
# closing: from open state, need D full (stones at 0,1,2), pistons retracted
p_close = bfs(s, lambda st: all(st[ix(x)]==1 for x in (0,1,2)), 60000)
print("close path", None if p_close in (None,'cap') else len(p_close))
if p_close and p_close!='cap':
    t = s
    for a in p_close:
        t = E.act(t, a[0], a[1]); print(a, row(t))
    print("final closed", row(t), "equal to start:", t == start)
