import sys
from grid2d import *
corner_out = [(-2,0,(1,0),True),(-2,2,(1,0),True),(4,0,(-1,0),True),(4,2,(-1,0),True),
              (0,-2,(0,1),True),(2,-2,(0,1),True),(0,4,(0,-1),True),(2,4,(0,-1),True)]
mid_frame = [(-1,1,(1,0),True),(3,1,(-1,0),True),(1,-1,(0,1),True),(1,3,(0,-1),True)]
stones = list(D) + [(-1,-1),(3,-1),(-1,3)]
start = make(stones, mid_frame + corner_out)
def d_empty(st): return all(st[ix(x,y)] == 0 for (x,y) in D)
path = search(start, d_empty, lambda s: sum(1 for (x,y) in D if s[ix(x,y)]!=0), 300000)
print('D-empty reachable:', 'cap' if path=='cap' else (None if path is None else len(path)))
if path and path != 'cap':
    st = start
    for a, ps in path:
        st = pulse(st, a)
    print(show(st))
