exec(open('work/t3.py').read().split("for sticky in")[0])
lab = Lab(chain(False))
lab.flip(10,2,Z)
ch = lab.step(30)
for t,pos,b,a in ch:
    print(t,pos,b.split('[')[0],'->',a.replace('piston','p').replace('observer','obs')[:60])
