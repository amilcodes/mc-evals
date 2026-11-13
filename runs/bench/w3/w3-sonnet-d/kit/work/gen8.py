exec(open('work/build8.py').read())
d=make8()
d.save('work/d8.json')
print(len(d.blocks), d.bbox())
