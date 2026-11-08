import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"cena":[12.5,0.0,None,7.0],"kusy":[2,4,3,0],"kod":["B","A","D","C"]}, index=["r2","r0","r3","r1"])
numeric = pd.DataFrame({"prvni":[1.5,0.0,-2.0],"druhy":[8.0,4.0,3.0]}, index=[20,0,10])
a=df.copy();a.loc["r0","cena"]=9.75
b=df.copy();b.loc["r3","kod"]="X"
d=numeric.copy();d.loc[0,"prvni"]=4.5

cases = [((df,"r0","cena",9.75),a), ((df,"r3","kod","X"),b), ((numeric,0,"prvni",4.5),d)]
check_cases(c, ns, 'nahrad_bunku', cases)
c.done()
