import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
a=pd.DataFrame({"kod":["B","A"],"hodnota":[2.0,None]},index=["x","y"])
b=pd.DataFrame({"kod":["B"],"hodnota":[0.0]},index=["x"])

cases = [((a,b),pd.DataFrame({"kod":["B","A","B"],"hodnota":[2.0,None,0.0]})), ((a.head(0),b),b.reset_index(drop=True)), ((a,b.head(0)),a.reset_index(drop=True)), ((a.head(0),b.head(0)),a.head(0).reset_index(drop=True)), ((a,a),pd.concat([a,a],ignore_index=True))]
check_cases(c, ns, 'spoj_radky', cases)
c.done()
