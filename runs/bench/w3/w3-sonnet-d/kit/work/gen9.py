exec(open('work/build9.py').read())
d=make9()
d.save('work/d9.json')
print(len(d.blocks), d.bbox())
