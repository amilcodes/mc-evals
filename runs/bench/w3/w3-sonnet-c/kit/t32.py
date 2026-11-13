for x in range(-4,3): print(x, lab.block(x,1,0))
print(lab.block(-1,0,0), lab.block(-1,-1,0))
for t,p,b,a in lab.history:
    if p in [(-3,1,0),(-4,1,0)] and t>=30: print(t,p,a[:60])
