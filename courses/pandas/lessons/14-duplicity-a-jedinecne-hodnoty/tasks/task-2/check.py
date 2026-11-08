import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"kod":["A","B","A","B","C","C"],"cena":[10.0,20.0,10.0,25.0,None,None]},index=["r5","r1","r4","r2","r0","r3"])
extra=pd.DataFrame({"kod":[None,"A",None,"A"],"x":[1,2,3,4]})

cases = [((df,["kod"]),df.loc[["r4","r2","r3"]]), ((df,["kod","cena"]),df.loc[["r1","r4","r2","r3"]]), ((df.head(0),["kod"]),df.head(0)), ((extra,["kod"]),extra.iloc[[2,3]])]
check_cases(c, ns, 'posledni_podle_klice', cases)
c.done()
