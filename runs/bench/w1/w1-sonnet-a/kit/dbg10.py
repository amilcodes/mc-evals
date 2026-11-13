from build5 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
lab.flip(-3,-2,3); lab.rest()
lab.flip(-3,-2,3); t0=lab.t
for i in range(22):
    lab.step(1)
    if 8<=i<=20: print(i+1, lab.block(-2,4,1)[-30:], '|', lab.block(-1,4,0)[-20:], '|', lab.block(-1,4,1)[-20:], '|', lab.block(0,4,1))
