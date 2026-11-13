exec(open('gen3.py').read())
d=full()
lab=Lab(d); print(lab.lost, lab.t)
ch=lab.step(30); print(len(ch), [c for c in ch][:10])
watch=[(-11,3,-6),(-5,1,0),(-4,1,0),(-19,3,-6),(-4,3,0),(-11,3,6),(-4,-1,0),(-2,-1,0)]
t0=lab.t
lab.flip(-10,3,0)
seen=len(lab.history)
lab.step(60)
for t,p,b,a in lab.history[seen:]:
    if p in watch or p in [(-3,1,0),(-1,-1,0)]:
        print(t-t0,p,a[:60])
