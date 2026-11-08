import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"cena":[30.0,10.0,10.0,None,5.0],"kusy":[1,2,4,3,5],"kod":["D","B","A","C","E"]}, index=["r3","r1","r4","r2","r0"])
named = df.iloc[[2,0]].rename_axis("zaznam")

cases = [((df,),df.reset_index(drop=True)), ((named,),named.reset_index(drop=True)), ((df.head(0),),df.head(0).reset_index(drop=True)), ((pd.DataFrame(index=["B","A"]),),pd.DataFrame(index=range(2)))]
check_cases(c, ns, 'obnov_index', cases)
c.done()
