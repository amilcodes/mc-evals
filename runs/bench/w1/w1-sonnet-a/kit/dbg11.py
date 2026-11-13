from build8 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
lab.flip(-3,-3,3); t0=lab.t
for i in range(45):
    for e in lab.step(1):
        if e[1] in ((1,4,0),(1,5,0),(3,3,0)) and 'moving' not in e[3]: print(e[0]-t0,'PIST',e[1],e[3][:36])
        if e[1] in ((1,4,1),(0,5,0),(3,5,0)) : print(e[0]-t0,e[1],e[3][:60])
