A=(-3,1,1); B=(-2,1,1); V=(-1,3,1)
def pulse(pos, ticks=2, rest=8):
    lab.flip(*pos)
    lab.step(ticks)
    lab.flip(*pos)
    lab.step(rest)
    print(pos, lab.view(z=0).split("\n",3)[3][:120])
for nm,p in [("A",A),("B",B),("A",A),("V",V),("B",B)]:
    print("pulse",nm)
    pulse(p)
