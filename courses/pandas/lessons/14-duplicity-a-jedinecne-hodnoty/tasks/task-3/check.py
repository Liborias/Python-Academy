import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"kod":["A","B","A","B","C","C"],"cena":[10.0,20.0,10.0,25.0,None,None]},index=["r5","r1","r4","r2","r0","r3"])
extra=pd.DataFrame({"kod":[None,"A",None]})

cases = [((df,["kod"]),pd.Series(True,index=df.index)), ((df,["kod","cena"]),pd.Series([True,False,True,False,True,True],index=df.index)), ((df.head(0),["kod"]),pd.Series([],index=df.index[:0],dtype=bool)), ((extra,["kod"]),pd.Series([True,False,True],index=extra.index))]
check_cases(c, ns, 'oznac_vsechny_duplicity', cases)
c.done()
