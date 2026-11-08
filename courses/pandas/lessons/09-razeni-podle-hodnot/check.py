import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"cena":[30.0,10.0,10.0,None,5.0],"kusy":[1,2,4,3,5],"kod":["D","B","A","C","E"]}, index=["r3","r1","r4","r2","r0"])
many = pd.DataFrame({"cena":[float(k % 4) for k in range(40)], "poradi":range(40)}, index=[f"r{k}" for k in range(40)])

cases = [((df,"cena",True),df.loc[["r0","r1","r4","r3","r2"]]), ((df,"cena",False),df.loc[["r3","r1","r4","r0","r2"]]), ((df,"kusy",False),df.loc[["r0","r4","r2","r1","r3"]]), ((df.head(0),"cena",True),df.head(0))]
cases.append(((many, "cena", True), many.sort_values("cena", kind="stable")))
check_cases(c, ns, 'serad_tabulku', cases)
c.done()
