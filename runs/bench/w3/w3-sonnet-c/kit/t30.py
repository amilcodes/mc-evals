exec(open('gen5.py').read())
d=full2()
lab=Lab(d,walls=True); print(lab.lost); lab.step(10)
LV=(-9,3,0)
def rowfull():
    b=lab.blocks()
    def ch(x,y=1):
        s=b.get((x,y,0),'air')
        return '.' if s=='air' else ('#' if s=='stone' else s[0])
    return ''.join(ch(x) for x in range(-3,3))+' G:'+b.get((-1,0,0),'air')[:5]+' A:'+b.get((-1,-1,0),'air')[-18:-14]
def go(n):
    t0=lab.t; lab.flip(*LV)
    marks=[]
    for k in range(0,n,2):
        lab.step(2)
        r=rowfull()
        if not marks or marks[-1][1]!=r: marks.append((lab.t-t0,r))
    for m in marks: print(m)
print('CLOSE'); go(90); print(lab.doorway())
print('OPEN'); go(110); print(lab.doorway())
