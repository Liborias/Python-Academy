import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
a=pd.DataFrame({"rano":[2.0,1.0]},index=["B","A"])
b=pd.DataFrame({"vecer":[5.0,6.0]},index=["C","B"])

cases = [((a,b),pd.DataFrame({"rano":[1.0,2.0,None],"vecer":[None,6.0,5.0]},index=["A","B","C"])), ((a.head(0),b),pd.concat([a.head(0),b],axis=1).sort_index()), ((a,b.head(0)),pd.concat([a,b.head(0)],axis=1).sort_index()), ((a.head(0),b.head(0)),pd.concat([a.head(0),b.head(0)],axis=1).sort_index())]
check_cases(c, ns, 'spoj_sloupce', cases)
c.done()
