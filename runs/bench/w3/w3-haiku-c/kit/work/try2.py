import sys, itertools
from grid2d import *
def run(name, pist, stones, cap=300000):
    start = make(stones, pist)
    path = search(start, is_open, hopen, cap)
    res = 'cap' if path=='cap' else (None if path is None else len(path))
    print(name, res, flush=True)
    return path
corner_out = [(-2,0,(1,0),True),(-2,2,(1,0),True),(4,0,(-1,0),True),(4,2,(-1,0),True),
              (0,-2,(0,1),True),(2,-2,(0,1),True),(0,4,(0,-1),True),(2,4,(0,-1),True)]
mid_frame = [(-1,1,(1,0),True),(3,1,(-1,0),True),(1,-1,(0,1),True),(1,3,(0,-1),True)]
mid_out = [(-2,1,(1,0),True),(4,1,(-1,0),True),(1,-2,(0,1),True),(1,4,(0,-1),True)]
stones = list(D) + [(-1,-1),(3,-1),(-1,3)]
# V1: frame middles + corner-edge pullers
p = run("V1 frame-mid + corner-out", mid_frame + corner_out, stones)
# V2: outer middles + corner-edge pullers (no frame pistons)
p = run("V2 outer-mid + corner-out", mid_out + corner_out, stones)
# V3: all
p = run("V3 all", mid_frame + mid_out + corner_out, stones)
