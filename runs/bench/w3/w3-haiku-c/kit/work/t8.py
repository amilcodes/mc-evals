import sys
from ext2 import *
corner_out=[(-2,0,(1,0),True),(-2,2,(1,0),True),(4,0,(-1,0),True),(4,2,(-1,0),True),(0,-2,(0,1),True),(2,-2,(0,1),True),(0,4,(0,-1),True),(2,4,(0,-1),True)]
mid_frame=[(-1,1,(1,0),True),(3,1,(-1,0),True),(1,-1,(0,1),True),(1,3,(0,-1),True)]
mid_out=[(-2,1,(1,0),True),(4,1,(-1,0),True),(1,-2,(0,1),True),(1,4,(0,-1),True)]
stones=list(D)+[(-1,-1),(3,-1),(-1,3)]
start=make(stones, mid_frame+mid_out+corner_out)
print(show(start))
path=astar(start, lambda s: hD(s)==0, hD, int(sys.argv[1]))
print('D-empty', 'cap' if path=='cap' else (None if path is None else len(path)))
if path and path!='cap':
    st=start
    for a,ps in path: st=act(st,a[0],a[1])
    print(show(st)); print([a for a,_ in path])
