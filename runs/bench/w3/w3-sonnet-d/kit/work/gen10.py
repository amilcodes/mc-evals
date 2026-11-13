exec(open('work/build10.py').read())
d=make10()
d.save('work/d10.json')
print(len(d.blocks), d.bbox())
