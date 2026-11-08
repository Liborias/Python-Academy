import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s = pd.Series([18.0,None,15.0,18.0,None],index=["B","D","A","C","E"],name="teplota",dtype="float64")

cases = [((s,True),s.loc[["D","E","A","B","C"]]), ((s,False),s.loc[["D","E","B","C","A"]]), ((s.iloc[0:0],False),s.iloc[0:0])]
many = pd.Series([float(k % 4) for k in range(40)], index=[f"r{k}" for k in range(40)], name="data")
cases.append(((many, True), many.sort_values(kind="stable", na_position="first")))
check_cases(c, ns, 'poradi_mereni', cases)
c.done()
