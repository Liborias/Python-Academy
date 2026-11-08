import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"cena":[30.0,10.0,10.0,None,5.0],"kusy":[1,2,4,3,5],"kod":["D","B","A","C","E"]}, index=["r3","r1","r4","r2","r0"])
extra = pd.DataFrame({"a":[1.0,1.0,None,0.0],"b":[None,2.0,3.0,9.0]},index=["p","s","r","q"])

cases = [((df,"cena","kusy"),df.loc[["r0","r4","r1","r3","r2"]]), ((df,"kusy","cena"),df.loc[["r3","r1","r2","r4","r0"]]), ((df.head(0),"cena","kusy"),df.head(0)), ((extra,"a","b"),extra.loc[["q","s","p","r"]])]
check_cases(c, ns, 'serad_podle_dvou', cases)
c.done()
