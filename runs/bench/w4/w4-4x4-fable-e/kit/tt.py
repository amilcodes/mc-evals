d=Design()
# lever -> dust -> observer -> dust pointing into B0 ; tower of 2 torches; output dust on top of B2
X=10
d.set(X-4,9,0,"stone"); d.set(X-4,10,0,"lever",face="floor",facing="north")
d.set(X-3,9,0,"stone"); d.set(X-3,10,0,"redstone_wire")
d.set(X-2,10,0,"observer",facing="west")
d.set(X-1,9,0,"stone"); d.set(X-1,10,0,"redstone_wire")
d.set(X,10,0,"stone")                       # B0
d.set(X,11,0,"redstone_torch",lit="true")   # T1
d.set(X,12,0,"stone")                       # B1
d.set(X,13,0,"redstone_torch",lit="false")  # T2
d.set(X,14,0,"stone")                       # B2
d.set(X,15,0,"redstone_wire")               # out
lab=Lab(d); print(lab.lost)
lab.rest(); print("settle", [h for h in lab.history])
for i in range(3):
    t0=lab.t; n=len(lab.history); lab.flip(X-4,10,0); lab.rest()
    print([(t-t0,p[1],a[-22:]) for t,p,b,a in lab.history[n:] if p[0]>=X-2])
