exec(open('ctl3.py').read())
d=ctrl()
lab=Lab(d); print(lab.lost); lab.rest()
LV=(-9,3,0)
def watch(cells, flipn):
    seen=len(lab.history); t0=lab.t
    lab.flip(*LV); lab.step(70)
    ev=[(t-t0,p,a) for t,p,b,a in lab.history[seen:] if p in cells]
    for e in ev:
        pw=e[2].split('power=')[1].split(']')[0].split(',')[0] if 'power=' in e[2] else e[2]
        print(e[0],e[1],pw)
Bend=(-6,3,9); Pend=(-6,3,-9)
print('rise'); watch([Bend,Pend],1)
print('fall'); watch([Bend,Pend],2)
