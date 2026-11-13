from build5 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
for p in [(-2,4,-1),(-1,4,-1),(-1,4,0),(-1,4,1),(-1,4,2),(-1,4,3),(-1,4,4),(-2,4,1),(-2,4,0),(-3,4,1)]:
    print(p, lab.block(*p))
lab.flip(-3,-2,3); lab.rest()
print('after close')
for p in [(-2,4,-1),(-1,4,0),(-1,4,1),(-2,4,1)]: print(p, lab.block(*p))
