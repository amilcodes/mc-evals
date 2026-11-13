exec(open('gen5.py').read())
d=full2()
d.save('door.json')
print(len(d.blocks), d.bbox())
