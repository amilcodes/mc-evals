exec(open('work/build6.py').read())
d=make6()
d.save('work/d6.json')
print(len(d.blocks), d.bbox())
