from build5 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
lab.flip(-3,-2,3); t0=lab.t
watch={(-3,6,0):'ON',(-3,6,-1):'r1',(-3,6,-2):'V0',(-2,5,-2):'d1',(-1,5,-2):'d2',(0,5,-2):'rep0',(1,5,-2):'rep1',(2,5,-2):'d3',(3,4,-2):'d4',(3,3,-1):'Vsink'}
for i in range(26):
    for e in lab.step(1):
        if e[1] in watch: print(e[0]-t0, watch[e[1]], e[3][:70])
