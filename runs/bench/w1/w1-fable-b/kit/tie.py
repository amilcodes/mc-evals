exec(open('core.py').read().split("d = core()")[0])
def mk(dW, dF):
    d = core()
    d.set(-2,-1,0,"stone"); d.set(-1,-2,0,"stone"); d.set(-1,-1,0,"repeater",facing="west",delay=1)
    d.set(0,-3,0,"glass"); d.set(0,-2,0,"redstone_wire")
    # manual pulse lever for Bk (south side z=1)... use repeater path instead:
    # common lever block at (10,0,0) region is far; build separate lines.
    # F path: lever LF at (-2,-1,3) -> stone (-2,-1,2)?? simpler: repeater at (-2,-1,1) facing south reading stone (-2,-1,2) with lever on it
    d.set(-2,-2,1,"stone"); d.set(-2,-1,1,"repeater",facing="south",delay=dF)
    d.set(-2,-1,2,"stone")
    # W path: stone (4,-1,0) powered by repeater at (4,-1,1) facing south reading stone (4,-1,2)
    d.set(4,-1,0,"stone"); d.set(4,-2,1,"stone"); d.set(4,-1,1,"repeater",facing="south",delay=dW)
    d.set(4,-1,2,"stone")
    # one lever each on the stones (top)
    d.set(-2,0,2,"lever",face="floor",facing="north")
    d.set(4,0,2,"lever",face="floor",facing="north")
    # manual drop pulse lever directly on Bk? use lever at (-3,-1,0) wall on Bk
    d.set(-3,-1,0,"lever",face="wall",facing="west")
    return d
def st(lab):
    return lab.doorway(), [lab.block(1,y,0)[:22] for y in (-3,-2,-1,0,1)], lab.block(2,-1,0)[:12], lab.entity
for dW,dF,off in [(4,4,0),(4,3,0),(3,4,0)]:
    lab = Lab(mk(dW,dF), walls=True)
    # drop pulse via manual lever: 2 ticks
    lab.flip(-3,-1,0); lab.step(2); lab.flip(-3,-1,0); lab.step(8)
    print("after drop", st(lab))
    lab.flip(-2,0,2); lab.flip(4,0,2); lab.step(30)
    print(dW,dF,"closed:", st(lab))
    # opening: both off simultaneously -> F falls at 2*dF+2, W at 2*dW
    lab.flip(-2,0,2); lab.flip(4,0,2); lab.step(30)
    print(dW,dF,"opened part:", st(lab))
