import importlib, build, sim; importlib.reload(build); importlib.reload(sim)
d = build.build()
lab = sim.run(d, flips=1, ticks=80)
