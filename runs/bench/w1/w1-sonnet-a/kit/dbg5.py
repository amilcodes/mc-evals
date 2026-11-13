from build3 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
lab.flip(-3,-2,3); lab.rest()
lab.flip(-3,-2,3); t0=lab.t
def corr():
    return ' '.join(f"{y}:"+''.join({'air':'.','stone':'#'}.get(lab.block(x,y,0).split('[')[0], 'P' if 'piston' in lab.block(x,y,0) else '?') for x in (1,2,3)) for y in (6,5,4,3,2,1))
last=None
for i in range(70):
    ch=lab.step(1)
    ev=[e for e in ch if e[1][0] in (1,2,3) and e[1][2]==0 and e[1][1] in (1,2,3,4,5) and 'moving' not in e[3]]
    if ev:
        print(lab.t-t0, corr())
