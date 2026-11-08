import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"cena":[12.5,0.0,None,7.0],"kusy":[2,4,3,0],"kod":["B","A","D","C"]}, index=["r2","r0","r3","r1"])
numeric = pd.DataFrame({"prvni":[1.5,0.0,-2.0],"druhy":[8.0,4.0,3.0]}, index=[20,0,10])
a=df.copy();a.loc[["r2","r1"],"cena"]=[10.0,4.5]
b=numeric.copy();b.loc[[20,0],"druhy"]=[9.5,5.5]

cases = [((df,"cena",7,-2.5),a), ((df,"cena",99,3),df), ((df,"cena",0,0),df), ((df.head(0),"cena",0,3),df.head(0)), ((numeric,"druhy",4,1.5),b)]
check_cases(c, ns, 'uprav_vybrane', cases)
c.done()
