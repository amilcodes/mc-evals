from build2 import make
d=make()
lab=Lab(d,walls=True)
print(lab.lost); lab.rest()
def corr():
    for y in (6,5,4,3,2,1):
        print(y,[ (x,lab.block(x,y,0)[:24]) for x in (0,1,2,3) if lab.block(x,y,0)!='air' and x in (1,2,3)])
corr()
lab.flip(-3,-2,3)
t0=lab.t
ch=[]
for i in range(60):
    c=lab.step(1)
    for e in c:
        if e[1][0] in (1,2,3) and e[1][1] in (3,4,5,2,1) and e[1][2]==0:
            print(e[0]-t0,e[1],e[2][:22],'->',e[3][:30])
lab.rest()
corr()
