exec(open('work/core.py').read())
lab=Lab(d,walls=True)
run([('L',singles)],lab)
print(lab.doorway())
for s in ['Q','F','Q']:
    pulse(lab,s); print(s,lab.doorway())
print(lab.view(z=0))
