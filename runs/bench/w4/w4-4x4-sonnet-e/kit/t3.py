import json
LEV={k:tuple(v) for k,v in json.load(open('m3lev.json')).items()}
lab=Lab('m3.json',walls=True); print(lab.lost)
def go(seq):
    for n in seq:
        if n=='P2f': lab.flip(*LEV['P2f'])
        else: lab.flip(*LEV['S1'+n]); lab.flip(*LEV['S2'+n])
        lab.rest()
seq=['P2h','P1','P2f','P1','V','P2h']
for r in range(3):
    go(seq); print('closed',lab.doorway(), lab.entity); go(list(reversed(seq))); print('open',lab.doorway())
