from build3 import make
d=make()
lab=Lab(d,walls=True)
print(lab.lost)
lab.rest()
def corr():
    return [(y,[(x,lab.block(x,y,0)[:14]) for x in (1,2,3) if lab.block(x,y,0)!='air']) for y in (6,5,4,3,2,1)]
print(corr())
lab.flip(-3,-2,3)
t0=lab.t
for i in range(80):
    c=lab.step(1)
    for e in c:
        if e[1][0] in (1,2,3) and e[1][1] in (3,4,5,2,1) and e[1][2]==0 and ('piston' in e[3] ):
            print(e[0]-t0,e[1],e[2][:22],'->',e[3][:34])
lab.rest()
print(corr())
