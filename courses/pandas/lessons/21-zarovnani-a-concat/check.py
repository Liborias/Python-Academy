import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
s=pd.Series([1.0,None,3.0],index=["B","A","C"],name="mereni",dtype="float64")

cases = [((s,["C","X","B"]),pd.Series([3.0,None,1.0],index=["C","X","B"],name="mereni",dtype="float64")), ((s,["A","A"]),pd.Series([None,None],index=["A","A"],name="mereni",dtype="float64")), ((s,[]),pd.Series([],index=[],name="mereni",dtype="float64")), ((s.rename("jine"),["B"]),s.rename("jine").reindex(["B"]))]
check_cases(c, ns, 'zarovnej_mereni', cases)
c.done()
