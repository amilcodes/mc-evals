from pdbuild import Design
d=Design("open")
lev={}
def add_lever_stone(name,x,y,z,side=1):
    d.set(x,y,z+side,"stone")
    d.set(x,y,z+2*side,"lever",face="wall",facing=("south" if side==1 else "north"))
    lev.setdefault(name,[]).append((x,y,z+2*side))
def piston(name,x,y,facing,side=1):
    d.set(x,y,0,"sticky_piston",facing=facing)
    add_lever_stone(name,x,y,0,side)
for p in [(-1,0),(-1,1),(-1,2),(0,3),(1,3),(2,3),(3,0),(3,1),(3,2),(0,-1),(1,-1),(2,-1)]:
    d.set(p[0],p[1],0,"stone")
piston('P00',0,-2,'up',1)
piston('Q',-2,1,'east',-1)
d.set(-2,1,1,"lever",face="wall",facing="west"); lev['Q'].append((-2,1,1))
piston('R',-3,1,'east',1)
piston('F',-1,3,'down',1)
piston('T2',0,4,'down',1)
piston('T',1,4,'down',1)
piston('T3',2,4,'down',1)
piston('E1',4,1,'west',1)
piston('B',1,-2,'up',1)
piston('P20',2,-2,'up',1)
singles=['P00','T2','T','T3','E1','B','P20']
def pulse(lab,name,on=2,settle=6):
    for p in lev[name]: lab.flip(*p)
    lab.step(on)
    for p in lev[name]: lab.flip(*p)
    lab.step(settle)
def lvl(lab,names):
    for n in names:
        for p in lev[n]: lab.flip(*p)
def run(seq,lab,show=True):
    for item in seq:
        if isinstance(item,tuple):
            lvl(lab,item[1]); lab.step(8)
        else: pulse(lab,item)
    if show: print(lab.doorway())
    return lab
