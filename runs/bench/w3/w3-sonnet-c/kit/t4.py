def pz(l,n=2,after=2):
    lab.flip(*l); lab.step(n); lab.flip(*l); lab.step(after)
pz(LB,2,2); lab.step(2); show()
pz(LA,2,2); lab.step(2); show()
# P on 8 ticks, B pulse at +4
lab.flip(*LP); lab.step(4); pz(LB,2,2); lab.flip(*LP); lab.step(8); show()
pz(LB,2,2); lab.step(4); show()
print(lab.doorway())
