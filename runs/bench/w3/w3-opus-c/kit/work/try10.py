import sys; sys.path.insert(0,'.'); sys.path.insert(0,'work')
import importlib
for mod in ["build6w","build5w"]:
  m=importlib.import_module(mod)
  for bnd in [((-4,4),(-2,4),(-2,0)), ((-5,4),(-2,4),(-2,0))]:
    for seed in range(2):
      try:
        B,t = m.build(bounds=bnd, seed=seed)
      except Exception as e:
        print("fail", mod, bnd, seed, e, flush=True); continue
      fn=f"work/d10_{mod}_{bnd[0][0]}.json"; B.d.save(fn); print("OK", fn, B.d.bbox(), flush=True)
      break
