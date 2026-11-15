lab = Lab(dS, walls=True)
Q = {"TL": ((0,3,0),(0,2,0)), "BL": ((0,0,0),(0,1,0)), "TR": ((3,3,0),(3,2,0)), "BR": ((3,0,0),(3,1,0))}
def run(lev):
    t0=lab.t; lab.flip(*lev); ch=lab.step(90)
    return [(c[0]-t0, c[1]) for c in ch]
def first(ch, cell): 
    ts=[t for t,p in ch if p==cell]; return min(ts) if ts else None
def last(ch, cell):
    ts=[t for t,p in ch if p==cell]; return max(ts) if ts else None
cR=run(LR); cC=run(LC); cS=run(LS); oS=run(LS); oC=run(LC); oR=run(LR)
print(lab.doorway())
res={}
for q,(corner,edge) in Q.items():
    r = dict(R_done=last(cR,edge), R_frame_done=None, C_edge_in=first(cC,edge), C_done=last(cC,corner), S_in=first(cS,corner),
             S_out=last(oS,corner), C_corner_in=first(oC,corner), C_edge_out=last(oC,edge), R_edge_in=first(oR,edge))
    res[q]=r; print(q, r)
# R closing: also the fetch stroke at frame cell must end before c arrives at edge: frame cells
for fc in ((-1,1,0),(-1,2,0),(4,1,0),(4,2,0)):
    print("frame", fc, "close last", last(cR,fc), "open last", last(oR,fc))
for fc in ((0,-1,0),(3,-1,0),(0,4,0),(3,4,0)):
    print("Cframe", fc, "close last", last(cC,fc), "open last", last(oC,fc))
print("ends", max(t for t,p in cR), max(t for t,p in cC), max(t for t,p in cS), max(t for t,p in oS), max(t for t,p in oC), max(t for t,p in oR))
