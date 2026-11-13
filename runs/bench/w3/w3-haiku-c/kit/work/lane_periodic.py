from lane_ext import *
from lane_cycle import row
def goal_D_empty_F(st): return all(st[ix(x)]==0 for x in (0,1,2)) and st[ix(-1)]==1 and st[ix(3)]==1
def goal_D_full(st): return all(st[ix(x)]==1 for x in (0,1,2))
def run(pw, pe, sx, sx2, cycles=4):
    pl = [(x,(1,0),True) for x in pw] + [(x,(-1,0),True) for x in pe]
    start = mk([0,1,2]+list(sx)+list(sx2), pl)
    s = start
    seq = []
    for c in range(cycles):
        p1 = bfs(s, goal_D_empty_F, 60000)
        if p1 in (None,'cap'): return ('open fail', c)
        for a in p1: s = E.act(s,a[0],a[1])
        p2 = bfs(s, goal_D_full, 60000)
        if p2 in (None,'cap'): return ('close fail', c)
        for a in p2: s = E.act(s,a[0],a[1])
        seq.append((len(p1), len(p2), row(s)))
    return seq, s == start, start
for cfg in [((-2,-3),(4,5,6),(-1,),()), ((-2,-3),(4,5,6,7),(),()), ((-2,-3,-4,-5),(4,5),(),())]:
    out = run(*cfg, cycles=4)
    print(cfg, out[0] if isinstance(out[0],str) else '')
    if not isinstance(out[0], str):
        for x in out[0]: print("   open", x[0], "close", x[1], x[2])
        print("   returns to start:", out[1])
