import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"kod":["A","B","A","B","C","C"],"cena":[10.0,20.0,10.0,25.0,None,None]},index=["r5","r1","r4","r2","r0","r3"])
other=pd.DataFrame({"x":[0,1,0],"y":["","A",""]},index=["C","A","B"])

cases = [((df,),df.loc[["r5","r1","r2","r0"]]), ((df.head(0),),df.head(0)), ((other,),other.loc[["C","A"]])]
check_cases(c, ns, 'odstran_duplicity', cases)
c.done()
