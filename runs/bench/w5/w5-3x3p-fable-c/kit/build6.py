exec(open("build5.py").read().split("d5 = build5()")[0])
def build6():
    d = build5()
    S = "stone"; G = "glass"; W = "redstone_wire"
    CROSS = dict(north="side", south="side", east="side", west="side")
    for p in [(0,5,0),(1,5,0),(2,5,0),(-1,5,0),(-2,5,0),(-2,5,1),(-1,5,1),(-1,4,0),(-2,4,0),(-2,4,1),(-2,3,1)]:
        d.remove(*p)
    d.set(2,4,0,S)                                   # replaces T2; strongly powered by Rb
    d.set(-2,3,1,"observer",facing="east")          # O_b watches note (-1,3,1)
    d.set(-1,3,1,"note_block")
    d.set(-1,4,1,W,**CROSS)
    d.set(0,4,1,S)
    d.set(1,4,1,"repeater",facing="east",delay=1)   # R3
    d.set(2,4,1,W)
    d.set(3,3,1,"repeater",facing="east",delay=1)   # Ra
    d.set(3,4,0,"repeater",facing="east",delay=4)   # Rb
    d.set(4,3,0,G); d.set(4,4,0,W)
    d.set(4,2,0,"sticky_piston",facing="west")      # R2
    d.set(-3,-2,1,"repeater",facing="east",delay=3)   # R_pre
    d.set(-3,0,1,"repeater",facing="west",delay=4)    # R_K
    d.set(-3,3,1,"repeater",facing="east",delay=3)    # R_A
    return d
d6 = build6(); d6.save("d6.json")
print(d6.bbox())
print(trace(d6, flips=2, limit=0))
r = test(d6); print(r)
d6.set(3,3,0,"stone"); d6.save("d6.json")
print(trace(d6, flips=2, limit=0))
r = test(d6); print(r)
