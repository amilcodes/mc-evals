d = Design()
def pist(x,y,face,sticky=True):
    d.set(x,y,0,"sticky_piston" if sticky else "piston",facing=face)
def lev(x,y):
    d.set(x,y,2,"stone"); d.set(x,y,1,"lever",face="wall",facing="north")
d.set(-1,1,0,"stone"); d.set(-1,2,0,"stone"); d.set(-1,0,0,"stone")
d.set(2,1,0,"stone") # placeholder Y
pist(-2,1,"east"); pist(-3,1,"east"); pist(-1,3,"down")
for p in [(-2,1),(-1,1),(-3,1),(-1,3)]: lev(*p)
lab = Lab(d)
A=(-3,1,1); B1=(-2,1,1); B2=(-1,1,1); V=(-1,3,1)
def row():
    s=lab.view(z=0)
    lines=[l for l in s.split("\n") if l.startswith("  y=")]
    return "\n".join(lines[1:5])
def pulse(pos, ticks=2, rest=8):
    lab.flip(*pos); lab.step(ticks); lab.flip(*pos); lab.step(rest)
import sys
def run(seq):
    for nm,p in seq:
        pulse(p); print(nm); print(row())
print("closing")
run([("A",A),("B2",B2),("A",A),("V",V),("B1",B1)])
