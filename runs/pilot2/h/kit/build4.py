def build4():
    d = build()
    S = "stone"
    d.set(3, 4, 0, S)
    d.set(3, 5, 0, "repeater", facing="east", delay=1)
    d.set(4, 5, 0, S)
    d.set(4, 5, 1, "observer", facing="south")
    d.remove(4, 3, 2)
    d.set(4, 4, 2, S); d.set(4, 5, 2, "redstone_wire")
    d.set(4, 4, 3, S); d.set(4, 5, 3, "redstone_wire")
    d.set(4, 2, 4, S); d.set(4, 3, 4, "redstone_wire")
    d.set(2, 4, 2, S)
    return d
d4 = build4()
d4.save("d4.json")
r = test(d4)
print(str(r)[:900])
