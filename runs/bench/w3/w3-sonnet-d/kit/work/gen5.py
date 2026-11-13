exec(open('work/build5.py').read())
d=make5()
d.save('work/d5.json')
print(len(d.blocks), d.bbox())
