exec(open('gen3.py').read())
d=full()
lab=Lab(d); lab.step(10)
t0=lab.t; seen=len(lab.history)
lab.flip(-10,3,0); lab.step(40)
show={(-4,1,0):'Pfeed',(-3,1,2):'domP',(-4,3,0):'trunkB0',(-2,3,0):'Bfeed',(-5,1,2):'dom51',(-5,1,-8):'Pstair',(-4,3,3):'trunk3',(-11,3,-6):'Rp_out'}
for t,p,b,a in lab.history[seen:]:
    if p in show or p in [(-3,1,0),(-2,1,0),(-3,1,1),(-1,-1,1)]:
        pw=a.split('power=')[1][:2] if 'power=' in a else a[:50]
        print(t-t0,show.get(p,p),pw)
