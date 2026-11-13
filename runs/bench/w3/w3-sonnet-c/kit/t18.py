exec(open('gen3.py').read())
d=full()
lab=Lab(d); print(lab.lost); lab.rest()
LV=(-10,3,0)
def row():
    return ''.join('.' if lab.block(x,1,0)=='air' else ('#' if lab.block(x,1,0)=='stone' else lab.block(x,1,0)[0]) for x in range(-3,3))
def go(n):
    t0=lab.t; lab.flip(*LV)
    marks=[]
    for k in range(0,n,2):
        lab.step(2)
        r=row()+' G:'+lab.block(-1,0,0)[:5]+' (-1,1):'+lab.block(-1,1,0)[:5]+' A:'+lab.block(-1,-1,0)[-18:-14]
        if not marks or marks[-1][1]!=r: marks.append((lab.t-t0,r))
    for m in marks: print(m)
print('CLOSE'); go(80); print(lab.doorway())
print('OPEN'); go(100); print(lab.doorway())
