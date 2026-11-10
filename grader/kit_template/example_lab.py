"""Worked example for the lab: what does a sticky piston do with an observer's short pulse?

Run it with:  ./pd py example_lab.py
Afterwards `pulser`, `lab` and `run_flip` are still defined, so you can carry on, for
example with:  ./pd py -c 'print(lab.view(z=0))'
"""


def pulser(x, y, z=0):
    """A lever, dust, an observer watching the dust, and a sticky piston with one stone.

    Along +x from (x, y, z): lever on a stone, dust on a stone, the observer, the piston, the
    stone it moves. Every flip of the lever changes the dust, so the observer fires once per flip.
    """
    d = Design()
    d.set(x, y - 1, z, "stone")
    d.set(x, y, z, "lever", face="floor", facing="north")
    d.set(x + 1, y - 1, z, "stone")
    d.set(x + 1, y, z, "redstone_wire")
    d.set(x + 2, y, z, "observer", facing="west")          # watches the dust, emits to the east
    d.set(x + 3, y, z, "sticky_piston", facing="east")
    d.set(x + 4, y, z, "stone")
    return d


def run_flip(lab, lever):
    """Flip, run until at rest, and report what the observer and the stone did."""
    start = lab.t
    seen = len(lab.history)
    lab.flip(*lever)
    lab.rest()
    for t, pos, before, after in lab.history[seen:]:
        if "observer" in after or pos[0] >= lever[0] + 4:
            print(f"  +{t - start:<2} {pos} {before} -> {after}")


X, Y = 4, 8                       # well clear of the doorway
lab = Lab(pulser(X, Y))
for flip in (1, 2):
    print(f"flip {flip}:")
    run_flip(lab, (X, Y, 0))
    print(f"  stone now at x = {[p[0] for p, s in lab.blocks().items() if s == 'stone' and p[1] == Y]}")
print(f"lab clock t={lab.t}; lab ticks left {lab.ticks_left}")
