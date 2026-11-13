from build3 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
lab.flip(-3,-2,3); t0=lab.t
watch={(-3,6,0):'ON',(-3,6,-1):'r1',(-3,6,-2):'r2',(-3,6,-3):'r3',(-3,6,-4):'V0',(0,6,-4):'Vrow0',(3,6,-4):'Vrow3',(4,6,-4):'Vrow4',(4,5,-5):'Vd1',(4,4,-6):'Vd2',(4,3,-7):'Vd3',(3,3,-7):'Vl7',(3,3,-6):'Vl6',(3,3,-3):'Vl3',(3,3,-2):'Vl2',(3,3,-1):'Vl1',(3,3,0):'V'}
for i in range(40):
    for e in lab.step(1):
        if e[1] in watch: print(e[0]-t0, watch[e[1]], e[3][:75])
