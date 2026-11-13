exec(open('core.py').read().split("d = core()")[0])
d = core()
S="stone"; W="redstone_wire"
# open-phase state after W' pulled N: emulate opening from closed is complex; instead start from "A at (1,1) alone": build custom
d.remove(1,-1,0); d.set(1,1,0,S)      # A in centre, N stored at (2,-1), P2 at rest, nothing at (1,-1)
# P1 feed + witness
d.set(2,-3,0,S); d.set(2,-2,0,W); d.set(2,-3,1,S); d.set(2,-2,1,W)
d.set(1,-3,1,"note_block"); d.set(1,-2,1,"observer",facing="down")
# S1 source: repeater at (2,-2,2) facing south reading stone (2,-2,3) with lever on top
d.set(2,-3,2,S); d.set(2,-2,2,"repeater",facing="south",delay=1)
d.set(2,-2,3,S); d.set(2,-2,4,"lever",face="wall",facing="south")
lab = Lab(d, walls=True); print(lab.lost)
lab.rest()
def st(): return lab.doorway(), [lab.block(1,y,0)[:24] for y in (-3,-2,-1,0,1)], lab.entity
t0=lab.t
lab.flip(2,-2,4); ch=lab.step(12)
for c in ch:
    if c[1][0]==1 or "observer" in c[3] or "note" in c[3]: print(c[0]-t0, c[1], c[2][:30], "->", c[3][:40])
print(st())
t0=lab.t
lab.flip(2,-2,4); ch=lab.step(14)
for c in ch:
    if c[1][0]==1 or "observer" in c[3] or "note" in c[3]: print(c[0]-t0, c[1], c[2][:30], "->", c[3][:40])
print(st())
