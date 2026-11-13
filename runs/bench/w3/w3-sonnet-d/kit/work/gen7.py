exec(open('work/build7.py').read())
d=make7()
d.save('work/d7.json')
print(len(d.blocks), d.bbox())
