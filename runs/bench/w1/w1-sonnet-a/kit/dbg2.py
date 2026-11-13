from build3 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
lab.flip(-3,-2,3); t0=lab.t
for i in range(70):
    c=lab.step(1)
    for e in c:
        if e[1][0] in (1,2,3) and e[1][2]==0 and e[1][1] in (1,2,3,4,5):
            print(e[0]-t0,e[1],e[3][:40])
