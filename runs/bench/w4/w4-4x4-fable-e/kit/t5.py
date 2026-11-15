exec(open("build3.py").read())
d=lefthalf()
for b in check(d): print(b)
levers={}
def lev(name,x,y,z):
    d.set(x,y-1,z,"stone"); d.set(x,y,z,"lever",face="floor",facing="north"); levers[name]=(x,y,z)
lev("Xr",-5,-4,-2); lev("Xc",-5,-4,3); lev("S",-2,-2,-3)
lab=Lab(d,walls=True); print("lost",lab.lost, d.bbox())
def go(name):
    t0=lab.t; n0=len(lab.history)
    lab.flip(*levers[name]); lab.rest()
    print(name, lab.doorway(), lab.entity, "ticks", lab.t-t0-20)
    return n0,t0
for n in ["Xr","Xc","S","S","Xc","Xr","Xr","Xc","S","S","Xc","Xr"]: go(n)
