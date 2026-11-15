d=Design(); X=10
d.set(X-2,9,0,"stone"); d.set(X-2,10,0,"lever",face="floor",facing="north")
d.set(X-1,9,0,"stone"); d.set(X-1,10,0,"redstone_wire")
d.set(X,9,0,"stone"); d.set(X,10,0,"redstone_wire")
# observer A watches dust from above? use first observer horizontal pulse source then vertical chain
d.set(X+1,10,0,"observer",facing="west")   # pulses into (X+2,10)
d.set(X+2,9,0,"stone"); d.set(X+2,10,0,"redstone_wire")
for y in (11,12,13,14): d.set(X+2,y,0,"observer",facing="down")
d.set(X+2,15,0,"redstone_wire")
lab=Lab(d); print(lab.lost)
for i in range(2):
    t0=lab.t; n=len(lab.history); lab.flip(X-2,10,0); lab.rest()
    print([(t-t0,p[1],a[-14:]) for t,p,b,a in lab.history[n:] if p[0]==X+2])
