exec(open('work/build4.py').read())
d=make3()
d.save('work/d4.json')
print(len(d.blocks), d.bbox())
