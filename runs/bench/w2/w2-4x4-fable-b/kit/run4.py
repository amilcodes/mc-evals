from pdlab import *
import importlib, build2, sim; importlib.reload(build2); importlib.reload(sim)
d = build2.build(); d.save("door2.json")
r = test(d); print(r.text[:1500])
