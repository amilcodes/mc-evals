import sys, heapq
from grid2d import *
Fp = []
for y in range(3):
    Fp += [(-1,y,(1,0),True),(3,y,(-1,0),True)]
for x in range(3):
    Fp += [(x,-1,(0,1),True),(x,3,(0,-1),True)]
outer = []
for y in range(3):
    outer += [(-2,y,(1,0),True),(4,y,(-1,0),True)]
for x in range(3):
    outer += [(x,-2,(0,1),True),(x,4,(0,-1),True)]
start = make(list(D), Fp + outer)
def hD(s): return sum(1 for (x,y) in D if s[ix(x,y)]!=0)
goal = lambda s: hD(s)==0
path = search(start, goal, hD, int(sys.argv[1]))
print("D-empty:", 'cap' if path=='cap' else (None if path is None else len(path)))
if path and path!='cap':
    st = start
    for a, ps in path:
        st = pulse(st, a)
    print(show(st))
    print([ (ix2:=None) for _ in []])
    import json
    print("moves", [a for a,_ in path])
