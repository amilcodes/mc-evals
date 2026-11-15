import importlib, sys
sys.path.insert(0,'work')
import mech; importlib.reload(mech)
d=mech.mech("closed")
IN_L={'IA1':(-3,4,1),'IB':(-4,4,0),'ICt':(-3,5,0),'ICb1':(-3,-2,0),'ICb2':(-1,-2,1),'IA2':(-4,2,1)}
def mir(p): return (3-p[0],p[1],p[2])
levers={}
for k,p in IN_L.items():
    for q,side in ((p,'L'),(mir(p),'R')):
        x,y,z=q
        d.set(x,y-1,z,"glass") if (x,y-1,z) not in d.blocks else None
        d.set(x,y,z,"lever",face="floor",facing="north")
        levers[k+side]=q
d.set(-3,3,1,"glass"); d.set(6,3,1,"glass")
lab=Lab(d,walls=True)
print("lost",lab.lost)
lab.rest()
print("start",lab.doorway())
def ev_for(opening):
    P={'A':[0,16,32],'B':[10,22],'C':[6] if opening else [28]}
    ev=[]
    base=10
    for side in 'LR':
        for t in P['A']:
            ev.append((base+t-6,'IA1'+side,'flip'))
            ev+= [(base+t-4,'IA2'+side,'flip'),(base+t-2,'IA2'+side,'flip')]
        for t in P['B']:
            ev.append((base+t-4,'IB'+side,'flip'))
        for t in P['C']:
            for k in ('ICt','ICb1','ICb2'):
                ev.append((base+t-2,k+side,'flip'))
    return sorted(ev)
def run(opening):
    t0=lab.t
    for t,k,_ in ev_for(opening):
        if t0+t>lab.t: lab.step(t0+t-lab.t)
        lab.flip(*levers[k])
    ok=lab.rest()
    return lab.doorway(), ok, lab.entity
for i in range(4):
    print(run(i%2==0))
