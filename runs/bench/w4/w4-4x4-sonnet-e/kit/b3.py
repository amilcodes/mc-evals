from b2 import *
import sys
def run2(base,stones,cells=(0,1),goalopen=None):
    w0=mk(base,stones); names=[b[2] for b in base]
    cl=lambda w: all(w.get((x,0))==('S',) for x in cells) and all(w.get((x,0)) is None for x in range(0,4) if x not in cells)
    fw=allpaths(w0,names,10)
    best=[]
    for k,p in fw.items():
        w={a:b for a,b in k}
        if not cl(w): continue
        bw=allpaths(w,names,10)
        for k2,p2 in bw.items():
            w2={a:b for a,b in k2}
            # open: doorway empty, frame (-1,0) is stone
            if all((x,0) not in w2 for x in range(0,4)) and w2.get((-1,0))==('S',):
                best.append((max(len(p),len(p2)),len(p),len(p2),p,p2,k2==key(w0)))
    best.sort(key=lambda t:(t[0],t[1]+t[2]))
    return best[:5]
print('row2 variant (pistons -5,-4; stones -3,-2,-1 +parked)')
for b in run2([((-5,0),'E','P1'),((-4,0),'E','P2'),((-1,2),'S','V1')],[(-3,0),(-2,0),(-1,0),(-1,1)]): print(b)
