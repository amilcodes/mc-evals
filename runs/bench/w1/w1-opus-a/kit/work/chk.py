exec(open('work/bfs5.py').read().split("alph=")[0])
import itertools
base=['B2p','B','Kp']
for r in range(3):
    for n in range(3,13):
        seq=[base[(r+i)%3] for i in range(n)]
        for c in closeds:
            o=run(c,seq,'open')
            if o is None or not isopen(o): continue
            c2=run(o,seq,'close')
            if c2==c: print('OK',n,seq,c[0])
