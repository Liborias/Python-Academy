import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
a=pd.DataFrame({"produkt":["X","C","A","X"],"kusy":[1,2,3,4]},index=[5,0,4,2])
b=pd.DataFrame({"produkt":["A","C"],"cena":[10.0,None]})

cases = [((a,b),a.iloc[[0,3]].reset_index(drop=True)), ((a,b.head(0)),a.reset_index(drop=True)), ((a.head(0),b),a.head(0).reset_index(drop=True))]
check_cases(c, ns, 'nesparovane_radky', cases)
c.done()
