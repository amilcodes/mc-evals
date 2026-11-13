from pdlab import *
import importlib, build; importlib.reload(build)
CH={'air':'.','stone':'#','sticky_piston':'P','piston_head':'h','moving_piston':'m','obsidian':'O','observer':'o','redstone_wire':'w'}
def snap(lab):
    s = {p:b.split('[')[0] for p,b in lab.blocks().items() if p[2]==0}
    rows=[]
    for y in range(5,-3,-1):
        rows.append(''.join(CH.get(s.get((x,y,0),'air'),'?') for x in range(-3,7)))
    return ' '.join(rows)
def run(d, flips=1, ticks=90, every=2, show=True):
    lab = Lab(d, walls=True)
    if lab.lost: print('LOST', lab.lost)
    lab.rest()
    out=[]
    for f in range(flips):
        lab.flip(-3,7,4)
        t0=lab.t
        prev=None
        for i in range(ticks//every):
            lab.step(every)
            s=snap(lab)
            if s!=prev and show: print(f'f{f} t{lab.t-t0:3d} {s}')
            prev=s
        lab.rest()
        print('rest', lab.doorway(), 'entity', lab.entity)
    return lab
