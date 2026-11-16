def run_sched(lab, events, total):
    """events: list of (t, pos) relative; flips lever at lab.t0+t"""
    t0 = lab.t
    ev = sorted(events)
    for t,p in ev:
        if t0+t > lab.t: lab.step(t0+t-lab.t)
        lab.flip(*p)
    if t0+total > lab.t: lab.step(t0+total-lab.t)
