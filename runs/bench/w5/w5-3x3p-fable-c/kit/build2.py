exec(open("build1.py").read().split("d1 = build()")[0])
def build2():
    d = build()
    S = "stone"; G = "glass"; W = "redstone_wire"
    # fix (b): note block observed by O_auto; A-sig path via (-4,3,1)
    d.remove(-4,1,1)
    d.set(-4,2,1,"note_block")
    d.set(-4,3,1,W)
    # fix (a): bypass R1 via x=5
    d.remove(4,2,0)
    d.set(5,1,1,G); d.set(5,2,1,W)
    return d
d2 = build2(); d2.save("d2.json")
print(d2.bbox())
print(trace(d2, flips=2, limit=0))
