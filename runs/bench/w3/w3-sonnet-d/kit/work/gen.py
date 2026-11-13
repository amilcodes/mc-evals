exec(open('work/build3.py').read())
d=make3()
d.save('work/d3.json')
print(len(d.blocks), d.bbox())
