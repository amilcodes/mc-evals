from build5 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
lab.flip(-3,-2,3); t0=lab.t
watch={(1,4,1):'Blane1',(1,4,4):'Blane4',(2,4,4):'R_D',(3,3,-1):'Vsink',(1,6,0):'Asink',(-2,4,0):'O2'}
for i in range(50):
    for e in lab.step(1):
        if e[1] in watch and ('wire' in e[3] or 'repeater' in e[3]): print(e[0]-t0, watch[e[1]], e[3][:62])
        if e[1] in ((1,4,0),(1,5,0),(3,3,0)) and 'moving' not in e[3]: print(e[0]-t0,'PIST',e[1],e[3][:40])
