exec(open("build4.py").read().split("d4 = build4()")[0])
def build5():
    d = build4()
    S = "stone"; G = "glass"; W = "redstone_wire"
    for p in [(4,-1,0),(4,0,0),(4,-1,1),(4,0,1),(4,1,1),(5,1,1),(5,2,1),(4,2,1),(4,3,1)]:
        d.remove(*p)
    d.set(4,-1,1,"redstone_torch",lit=True)
    d.set(4,0,1,S)
    d.set(4,1,1,"redstone_torch",lit=False)
    d.set(4,2,1,S)
    d.set(4,3,1,W)
    d.set(-3,-2,1,"repeater",facing="east",delay=2)   # R_pre
    d.set(-3,0,1,"repeater",facing="west",delay=4)    # R_K
    d.set(0,4,1,"repeater",facing="east",delay=3)     # Rb
    d.set(-3,3,1,"repeater",facing="east",delay=4)    # R_A
    return d
d5 = build5(); d5.save("d5.json")
print(d5.bbox())
print(trace(d5, flips=2, limit=0))
r = test(d5); print(r)
