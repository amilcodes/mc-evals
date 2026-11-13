from sa_bfs import best_reach
from bfs2d import DOOR, RING, toggle, make_env
from collections import deque
import sys
box=((-2,3),(-2,3))
pist=[((-2, 3), 's', True), ((3, -2), 's', True), ((-2, 2), 'e', True), ((0, -2), 's', True), ((-2, 1), 'e', True), ((2, -2), 's', True), ((-1, -2), 's', True), ((1, -2), 's', True)]
spares=[(-2, 0), (-1, -1), (3, -1)]
b=best_reach(pist,spares,box,limit=3000)
print('best', b[0], sorted(b[1][0]))
# which door cells can ever empty
inb=make_env(box)
ef0=tuple(False for _ in pist)
S0=(frozenset(DOOR|set(spares)),ef0)
seen={S0}; q=deque([S0]); empt=set(); n=0
while q and n<20000:
    s=q.popleft(); n+=1
    empt |= {c for c in DOOR if c not in s[0]}
    for i in range(len(pist)):
        r=toggle(s[0],s[1],pist,i,inb)
        if r is None or r in seen: continue
        seen.add(r); q.append(r)
print('states',n,'door cells that can empty', sorted(empt))
