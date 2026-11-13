exec(open('search4.py').read().split("def run(state,seq)")[0])
def M(st): return ext_ret_P(st)
s0={(-4,1):('P','sp','e'),(-3,1):('B','sp','e'),(-2,1):('G','stone',None),(-1,1):('S','stone',None)}
st=s0
for i in range(6):
    st=M(st)
    print(i+1, sorted((v[0],p) for p,v in st.items()))
