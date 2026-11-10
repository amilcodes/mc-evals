# Trial of the lab on the hard part of a 3x3 door: the two-step travel into the centre cell.
# Two sticky pistons stacked above the middle column, each with its own lever on a block beside it.


def extender():
    d = Design()
    d.set(1, 5, 0, "sticky_piston", facing="down")        # B, the back piston
    d.set(1, 4, 0, "sticky_piston", facing="down")        # F, the front piston
    d.set(1, 3, 0, "stone")                               # the stone that must end up in (1, 1, 0)
    d.set(2, 5, 0, "stone")
    d.set(3, 5, 0, "lever", face="wall", facing="east")   # powers the block beside B
    d.set(0, 4, 0, "stone")
    d.set(-1, 4, 0, "lever", face="wall", facing="west")  # powers the block beside F
    return d


LB, LF = (3, 5, 0), (-1, 4, 0)


def column(lab):
    return {y: lab.block(1, y, 0).split("[")[0] for y in (5, 4, 3, 2, 1)}


lab = Lab(extender())
print("placed, lost:", lab.lost)
lab.flip(*LB)
lab.rest()
print("B lever on      ->", column(lab))
lab.flip(*LF)
lab.rest()
print("then F lever on ->", column(lab))
lab.flip(*LF)
lab.rest()
print("F lever off     ->", column(lab))
lab.flip(*LB)
lab.rest()
print("B lever off     ->", column(lab))
print("entity:", lab.entity, " clock:", lab.t)
