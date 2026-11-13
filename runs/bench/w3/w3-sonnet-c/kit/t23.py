lab=Lab(d); lab.step(10)
t0=lab.t; lab.flip(*LV); seen=len(lab.history)
lab.step(40)
cells=[(-11,3,-4),(-11,3,-5),(-11,3,-6),(-11,3,-8),(-9,3,-8),(-8,3,-8),(-5,1,-8),(-5,1,-4),(-5,1,0),(-4,1,0)]
for t,p,b,a in lab.history[seen:]:
    if p in cells: print(t-t0,p,a.split('[')[0], a.split('power=')[1][:2] if 'power=' in a else a[a.find('['):][:40])
