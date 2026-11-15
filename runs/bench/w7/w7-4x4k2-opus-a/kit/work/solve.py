ORDER=[(0,1),(-1,1),(-2,1),(-3,1),(-4,1),(-5,1),(-6,1),(-7,1),(-7,0),(-6,0),(-5,0),(-4,0),(-3,0),(-2,0),(-1,0),(0,0)]
FIXED={(-2,1):"b",(-2,0):"b",(-7,1):"d",(-7,0):"d"}
def solve(taps, n, m_b, n_t, extra=0, DD=None):
    """taps: name->(x,z); n: name->path len. returns line dict or None"""
    D=2+2*m_b-2*n_t+extra if DD is None else DD
    if D<0: D=0
    for O in range(0,200,2):
        P={'A1':O,'A4':O+16+D,'A7':O+32+2*D,'B3':O+10+D,'B5':O+22+D}
        req={}
        for k,v in P.items():
            lat=16+2*n[k] if k[0]=='A' else 10+2*n[k]
            req[taps[k]]=v-lat
        req[(XN,1)]=O+6-4-2*n_t
        req[(XN,0)]=O+28+D-4-2*n_t
        # walk the line
        t=0; line={}; ok=True; prev_t=0
        # T of an element = output time. lever at t=0.
        cons=[(i,req[p]) for i,p in enumerate(ORDER) if p in req]
        # greedy: between constraints distribute
        last_i=-1; last_t=0
        for i,rt in cons:
            seg=ORDER[last_i+1:i+1]
            # elements in seg: each repeater adds 2..8, dust/block adds 0 (block: same time as prev)
            diff=rt-last_t
            if diff<0 or diff%2: ok=False;break
            reps=[p for p in seg if p not in FIXED]
            tapset=set(taps.values())
            must=[p for p in reps if p in tapset or p==ORDER[i]]
            opt=[p for p in reps if p not in must]
            assign={p:1 for p in must}
            for p in opt: assign[p]=0
            need=diff-2*len(must)
            if need<0: ok=False;break
            for p in must+opt:
                while need>0 and assign[p]<4:
                    assign[p]+=1; need-=2
            if need!=0: ok=False;break
            for p,dv in assign.items():
                line[p]=('r',dv) if dv>0 else ('d',0)
            last_i=i; last_t=rt
        if not ok: continue
        for p in ORDER[last_i+1:]:
            if p not in FIXED: line[p]=('r',1)
        for p,k in FIXED.items(): line[p]=(k,0)
        # check: taps must be repeaters or dust (watched change) and dust not on both legs same x
        bad=False
        for x in range(-7,1):
            if line.get((x,1),('',0))[0]=='d' and line.get((x,0),('',0))[0]=='d' and x!=-7: bad=True
        if bad: continue
        return O,D,line
    return None
