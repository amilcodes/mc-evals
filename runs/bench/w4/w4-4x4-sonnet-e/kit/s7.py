from s6 import *
home.update({'X':(-5,0)})
import itertools
base=[((-3,0),'E','P1'),((-2,0),'E','P2'),((-1,2),'S','V1'),((-5,0),'E','X')]
w0=mk(base,[(-1,0),(-1,1)]); names=['P1','P2','V1','X']
cl=[]
for n in range(1,8):
    for seq in itertools.product(names,repeat=n):
        w1=run2(w0,seq)
        if closed(w1): cl.append((seq,w1))
print('closing',len(cl))
best=None
cl.sort(key=lambda t:len(t[0]))
for seq,w1 in cl[:300]:
    for n in range(1,9):
        found=False
        for sq in itertools.product(names,repeat=n):
            if run2(w1,sq)==w0:
                print(len(seq),len(sq),seq,sq); found=True; break
        if found: break
