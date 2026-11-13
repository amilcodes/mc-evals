import sys, itertools, json; sys.path.insert(0,'.'); sys.path.insert(0,'work')
import build5
cors = [
 [(-2,3,-1),(-2,4,-1),(-2,2,-1),(-2,3,0),(-2,-1,0),(-2,-2,0),(-3,4,-1),(-4,4,-1),(-3,4,0),(-2,4,0)],
 [(-2,3,-1),(-2,4,-1),(-2,3,0),(-3,4,-1)],
 [(-2,3,-1),(-2,4,-1),(-2,2,-1),(-2,3,0),(-2,-1,0),(-2,-2,0)],
 [(-2,3,-1),(-2,4,-1),(-2,3,0),(-3,4,-1),(-3,4,0),(-2,4,0),(-4,4,-1),(-4,4,0)],
]
k=0
for bnd in [((-4,4),(-2,4),(-2,0)), ((-5,4),(-2,4),(-2,0))]:
  for ci,cor in enumerate(cors):
    for l1o in (0,1):
      for seed in range(4):
        try:
            B,t = build5.build(bounds=bnd, seed=seed, corridor=cor, l1order=l1o)
        except Exception as e:
            continue
        fn=f"work/c_{k}.json"; B.d.save(fn); k+=1
        print("OK", fn, bnd, ci, l1o, seed, B.d.bbox(), flush=True)
        break
