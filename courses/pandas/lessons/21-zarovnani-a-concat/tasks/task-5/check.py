import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
s=pd.Series([1.0,None,3.0],index=["B","A","C"],name="mereni",dtype="float64")
b=pd.Series([0.0],index=["B"],name="mereni",dtype="float64")

cases = [((s,b),pd.Series([1.0,None,3.0,0.0],index=["B","A","C","B"],name="mereni",dtype="float64")), ((s.iloc[:0],b),b), ((s,s.iloc[:0]),s), ((s.rename("X"),b.rename("X")),pd.concat([s.rename("X"),b.rename("X")]))]
check_cases(c, ns, 'spoj_serie', cases)
c.done()
