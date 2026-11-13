lab=Lab(d); lab.rest()
lab.flip(*LP); 
for c in lab.step(4): print(c)
print('--B pulse')
lab.flip(*LB)
for c in lab.step(3): print(c)
print(lab.look(at=(-2,3,0)) if False else '')
print(lab.block(-2,3,0), lab.block(-1,3,0), lab.block(-1,2,0), lab.block(-2,3,1), lab.block(-2,3,2))
