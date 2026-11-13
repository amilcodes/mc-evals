d = Design()
# top corridor (facing down) at column x=1
d.set(1,5,0,"sticky_piston",facing="down")   # A
d.set(1,4,0,"sticky_piston",facing="down")   # B
d.set(3,3,0,"sticky_piston",facing="west")   # V
d.set(1,3,0,"stone")  # S
d.set(2,3,0,"stone")  # X
# feeds on -z side
# A: dust on top at (1,6,0), connected from (1,6,-1); support (1,5,-1)
d.set(1,6,0,"redstone_wire"); d.set(1,5,-1,"stone"); d.set(1,6,-1,"redstone_wire")
d.set(1,6,-2,"redstone_wire"); d.set(1,5,-2,"stone")
# B: dust (1,4,-1) aimed south into B, connected from (1,4,-2); supports are walls
d.set(1,4,-1,"redstone_wire"); d.set(1,4,-2,"redstone_wire"); d.set(1,4,-3,"redstone_wire")
# V: dust (3,3,-1),(3,3,-2)
d.set(3,3,-1,"redstone_wire"); d.set(3,3,-2,"redstone_wire"); d.set(3,3,-3,"redstone_wire")
# levers: attach to floor of stones below? use lever at end cells: (1,6,-3) etc.
d.set(1,5,-3,"stone"); d.set(1,6,-3,"lever",face="floor",facing="north")
d.set(1,4,-4,"lever",face="floor",facing="north")   # support (1,3,-4) is wall
d.set(3,3,-4,"lever",face="floor",facing="north")   # support (3,2,-4) wall
lab = Lab(d, walls=True)
print(lab.lost)
LA=(1,6,-3); LB=(1,4,-4); LV=(3,3,-4)
def show():
    s=lab.view(z=0).split("\n")
    out=[l for l in s if l.startswith("  y=") and any(f"y=  {k}" in l or f"y= {k}" in l for k in (6,5,4,3,2,1))]
    print("\n".join(out))
def pulse(p, ticks=2, rest=8):
    lab.flip(*p); lab.step(ticks); lab.flip(*p); lab.step(rest)
for nm,p in [("B",LB),("V",LV),("A",LA),("A",LA)]:
    pulse(p); print(nm); show()
