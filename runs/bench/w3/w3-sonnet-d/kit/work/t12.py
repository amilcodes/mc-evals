exec(open('work/t11.py').read().split("sched=")[0])
lab.step(20); 
lab.flip(*LR); lab.step(12); print('R edge', rows())
lab.flip(*LQ); lab.step(2); lab.flip(*LQ)
for k in range(10):
    lab.step(1); print(k,rows())
print(lab.block(-1,1,-1), lab.block(-2,1,-1), lab.block(-3,1,-1), lab.block(-1,1,0))
