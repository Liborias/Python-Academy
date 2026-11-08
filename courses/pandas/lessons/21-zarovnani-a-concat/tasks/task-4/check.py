import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
a=pd.DataFrame({"B":[1.0,2.0],"A":[3.0,4.0]},index=["x","y"])
b=pd.DataFrame({"A":[5.0],"C":[6.0]},index=["z"])

cases = [((a,b),pd.DataFrame({"A":[3.0,4.0,5.0]})), ((a,a[["A","B"]]),pd.concat([a,a[["A","B"]]],join="inner",ignore_index=True)), ((a[["B"]],b[["C"]]),pd.DataFrame(index=range(3))), ((a.head(0),b),b[["A"]].reset_index(drop=True))]
check_cases(c, ns, 'spolecne_sloupce', cases)
c.done()
