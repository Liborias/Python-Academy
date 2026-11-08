import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"cena":[30.0,10.0,10.0,None,5.0],"kusy":[1,2,4,3,5],"kod":["D","B","A","C","E"]}, index=["r3","r1","r4","r2","r0"])

cases = [((df,2),df.loc[["r0","r1"]]), ((df,0),df.iloc[0:0]), ((df,99),df.loc[["r0","r1","r4","r3","r2"]]), ((df.head(0),2),df.head(0))]
check_cases(c, ns, 'nejlevnejsi', cases)
c.done()
