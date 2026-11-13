lab=Lab(d,walls=True); lab.step(10)
lab.flip(*LV); lab.step(70)
t1=lab.t; seen=len(lab.history)
lab.flip(*LV); lab.step(60)
cells={(-16,3,0):'nA',(-21,3,0):'nTb',(-14,3,0):'nD2',(-16,3,4):'A4a',(-21,3,4):'A4b',(-2,-1,0):'Afeed',(-14,3,-4):'Plev',(-4,1,0):'Pfeed',(-16,3,3):'repA',(-21,3,3):'repTb'}
for t,p,b,a in lab.history[seen:]:
    if p in cells: print(t-t1,cells[p], a.split('power=')[1][:2] if 'power=' in a else a[:60])
