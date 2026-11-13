print(lab.block(-10,3,0), lab.block(-11,3,0), lab.block(-10,2,0))
print(len(lab.history)); 
for h in lab.history[:15]: print(h)
print(lab.view(z=0))
