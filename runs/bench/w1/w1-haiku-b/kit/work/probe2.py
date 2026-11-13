# Hand-built candidate: exchange pistons on all four sides, center via chain. Test relaxed reachability.
from sa_bfs import best_reach
import sys
box=((-2,4),(-2,4))
pist=[]
for r in range(3):
    pist.append(((-2,r),'e',True))  # left column pulls
    pist.append(((4,r),'w',True))   # right
for c in range(3):
    pist.append(((c,-2),'s',True))  # top
    pist.append(((c,4),'n',True))   # bottom
spares=[(-2,-2),(4,-2),(-2,4)]
b=best_reach(pist,spares,box,limit=20000)
print('best',b[0], sorted(b[1][0]))
