import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"skupina":["D","B","A","C"],"radky":[1,2,3,4],"prumer":[None,10.0,10.0,0.0]},index=["r0","r1","r2","r3"])

cases = [((df,),df.loc[["r2","r1","r3","r0"]].reset_index(drop=True)), ((df.head(0),),df.head(0).reset_index(drop=True))]
check_cases(c, ns, 'serad_prehled', cases)
c.done()
