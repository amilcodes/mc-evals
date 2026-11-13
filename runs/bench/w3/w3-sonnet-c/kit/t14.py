exec(open('gen2.py').read())
d=build(); controller(d)
lab=Lab(d); print(lab.lost)
