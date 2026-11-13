from build5 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
lab.flip(-3,-2,3); lab.rest()
lab.flip(-3,-2,3); t0=lab.t
watch={(-2,4,1):'DL2',(-2,4,0):'O2',(-1,4,0):'Rp',(-1,4,1):'comp',(-1,4,2):'RB1',(-1,4,3):'OB',(-1,4,4):'G0',(0,4,4):'G1',(1,4,1):'Blane1',(1,4,4):'Blane4',(2,4,4):'R_D'}
for i in range(60):
    for e in lab.step(1):
        if e[1] in watch: print(e[0]-t0, watch[e[1]], e[3][:60])
        if e[1] in ((1,4,0),(1,5,0),(3,3,0)) and 'moving' not in e[3]: print(e[0]-t0,'PIST',e[1],e[3][:40])
