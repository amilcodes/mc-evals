d = Design("open")
d.set(-1,2,0,"stone"); d.set(-1,3,0,"stone")
d.set(-2,2,0,"sticky_piston",facing="east")
d.set(-3,2,0,"sticky_piston",facing="east")
d.set(-1,4,0,"sticky_piston",facing="down")
d.set(-3,2,-2,"stone"); d.set(-3,2,-1,"lever",face="wall",facing="south")
d.set(-2,2,2,"stone"); d.set(-2,2,1,"lever",face="wall",facing="north")
d.set(-2,2,-1,"lever",face="wall",facing="west")
d.set(-1,4,2,"stone"); d.set(-1,4,1,"lever",face="wall",facing="north")
lab = Lab(d, walls=True)
print(lab.lost)
B=(-3,2,-1); FB=(-2,2,1); FF=(-2,2,-1); K=(-1,4,1)
def row():
    return "".join({"stone":"#","air":"."}.get(lab.block(x,2,0).split("[")[0], "?") for x in range(-1,4)) + " p3=" + lab.block(-1,3,0)[:5]
def act(lv, n):
    lab.flip(*lv); lab.step(n); print(lv, lab.t, row(), lab.block(-2,2,0)[:40], lab.block(-1,2,0)[:40])
# close: Fb short pulse
lab.flip(*FB); lab.step(2); lab.flip(*FB); lab.step(6); print("drop", row())
act(K, 5)
act(FB, 5)
print("closed?", row(), lab.entity)
