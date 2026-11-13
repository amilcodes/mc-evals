import sys
from grid2d import *
# closed: D full. pistons: frame-middle sticky pistons facing inward, plus outer pullers for edges
pist = []
for y in range(3):
    pist.append((-2, y, (1,0), True)); pist.append((4, y, (-1,0), True))
for x in range(3):
    pist.append((x, -2, (0,1), True)); pist.append((x, 4, (0,-1), True))
stones = list(D) + [(-1,-1),(3,-1),(-1,3)]   # 12 stones; three parked at corners
start = make(stones, pist)
print(show(start))
cap = int(sys.argv[1])
path = search(start, is_open, hopen, cap)
print("result", 'cap' if path=='cap' else (None if path is None else len(path)))
if path and path!='cap':
    for a, ps in path: print(a, decode(ps[a]) if False else '')
