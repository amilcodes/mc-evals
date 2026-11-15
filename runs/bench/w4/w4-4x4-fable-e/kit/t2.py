exec(open("mech.py").read())
d=Design(); lefthalf(d)
levers={}
def level(name,x,y,z):
    if (x,y,z)!=(1,5,-3): d.set(x,y-1,z,"stone")
    d.set(x,y,z,"lever",face="floor",facing="north"); levers.setdefault(name,[]).append((x,y,z))
def pulse(name,feed,dx,dz):
    x,y,z=feed
    # observer adjacent to feed at (x+dx,z+dz), watching away; dust then lever further
    fac={(-1,0):"west",(1,0):"east",(0,-1):"north",(0,1):"south"}[(dx,dz)]
    d.set(x+dx,y,z+dz,"observer",facing=fac)
    W(d,x+2*dx,y,z+2*dz)
    level(name,x+3*dx,y,z+3*dz)
pulse("Pr",(-4,2,1),-1,0)
level("Ar",-3,2,-3)
pulse("Pc",(-2,-1,1),0,1); pulse("Pc",(-3,5,1),0,1)
level("Ac",0,-3,-2); level("Ac",0,7,-3)
level("S",-2,0,-3); level("S",-2,4,-3); level("S",1,-2,-3); level("S",1,5,-3)
lab=Lab(d,walls=True); print("lost",lab.lost)
def go(name):
    for p in levers[name]: lab.flip(*p)
    lab.rest()
    print(name, lab.doorway(), lab.entity)
for n in ["Pr","Ar","Pr","Pc","Ac","Pc","S"]: go(n)
print(lab.view(z=0))
for n in ["S","Pc","Ac","Pc","Pr","Ar","Pr"]: go(n)
print(lab.view(z=0))
