def robust(dd, lever, offsets=(0,1,2,3,5,7,11,0,1,3), verbose=True):
    lab = Lab(dd, walls=True)
    lab.rest()
    ok = True
    expect_closed = False
    for i,off in enumerate(offsets):
        if off: lab.step(off)
        lab.flip(*lever)
        t0 = lab.t
        rested = lab.rest(200)
        expect_closed = not expect_closed
        dw = lab.doorway()
        good = rested and dw == ("###/###/###" if expect_closed else ".../.../...")
        if verbose: print(i, off, dw, "rest" if rested else "NOREST", lab.t - t0 - 20, "OK" if good else "BAD", lab.entity)
        ok = ok and good
    return ok
print(robust(d5, (1,4,1)))
