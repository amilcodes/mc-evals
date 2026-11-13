lab=Lab(d); lab.rest()
lab.flip(*LV); lab.step(100)
pw={p:s for p,s in lab.blocks().items() if 'redstone_wire' in s and 'power=0' not in s}
for p in sorted(pw): print(p, pw[p].split('power=')[1][:2])
