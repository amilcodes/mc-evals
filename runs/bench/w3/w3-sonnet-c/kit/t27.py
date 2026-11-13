exec(open('gen3.py').read())
d=full()
lab=Lab(d,walls=True); print(lab.lost); lab.step(10)
t0=lab.t; seen=len(lab.history)
lab.flip(-10,3,0); lab.step(34)
show={(-4,1,0):'Pfeed',(-3,1,2):'domP',(-1,3,3):'trunk3',(-2,2,1):'B1dust',(-1,3,0):'B2dust',(-5,1,2):'dom51'}
for t,p,b,a in lab.history[seen:]:
    if p in show or p in [(-3,1,0),(-2,1,0),(-3,1,1),(-1,-1,1),(-1,-1,0),(-1,1,0),(0,1,0),(1,1,0)]:
        pw=a.split('power=')[1][:2] if 'power=' in a else a[:52]
        print(t-t0,show.get(p,p),pw)
