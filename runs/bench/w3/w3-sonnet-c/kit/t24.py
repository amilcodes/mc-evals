for t,p,b,a in lab.history[seen:]:
    if p[2] in (-3,-4,-5,-6) and p[0] in (-11,-10,-9): print(t-t0,p,a[:70])
