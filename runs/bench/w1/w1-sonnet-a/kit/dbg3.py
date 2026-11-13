from build3 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
print(lab.lost)
lab.flip(-3,-2,3); t0=lab.t
watch={(-3,6,3):'N0',(0,6,3):'row0',(3,6,3):'row3',(3,5,4):'dsc1',(3,4,5):'dsc2',(2,4,5):'R_D',(1,4,5):'lane5',(1,4,2):'lane2',(1,4,1):'lane1',
       (-3,6,-1):'rV1',(-3,6,-4):'V0',(4,6,-4):'Vrow4',(4,3,-7):'Vd3',(3,3,-5):'Vl',(3,3,-1):'Vl1',
       (-2,4,1):"DL2",(-1,4,1):"comp",(-1,4,2):"RB1",(-1,4,3):"RB2",(-1,4,4):"OB",(-1,4,5):"G0",(-1,4,0):"cin"}
for i in range(50):
    for e in lab.step(1):
        if e[1] in watch: print(e[0]-t0, watch[e[1]], e[3][:70])
