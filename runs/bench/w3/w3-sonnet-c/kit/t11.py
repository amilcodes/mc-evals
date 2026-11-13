def row(): return ''.join('.' if lab.block(x,1,0)=='air' else ('#' if lab.block(x,1,0)=='stone' else lab.block(x,1,0)[0]) for x in range(-3,3))
for n in (1,2,3):
    lab=Lab(d); lab.rest()
    lab.flip(*LP); lab.step(4)
    lab.flip(*LB); lab.step(n); lab.flip(*LB)
    ch=lab.step(8)
    print(n,row(),[(t,p) for t,p,b,a in ch if p[1]==1])
