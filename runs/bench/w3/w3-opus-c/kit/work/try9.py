import sys; sys.path.insert(0,'.'); sys.path.insert(0,'work')
import build6
for bnd in [((-5,4),(-2,4),(-2,0)), ((-4,4),(-2,4),(-2,0))]:
  for seed in range(3):
    try:
        B,t = build6.build(bounds=bnd, seed=seed)
    except Exception as e:
        print("fail", bnd, seed, e, flush=True); continue
    B.d.save("work/d9.json"); print("OK", seed, B.d.bbox(), flush=True); sys.exit(0)
