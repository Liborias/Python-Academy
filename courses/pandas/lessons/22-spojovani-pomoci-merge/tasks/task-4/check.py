import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
a=pd.DataFrame({"kod":["B","A","B"],"kusy":[1,2,3]},index=[4,1,3])
b=pd.DataFrame({"id":["A","C"],"nazev":["Čaj","Voda"]})

cases = [((a,b),a.merge(b,left_on="kod",right_on="id",how="left",sort=False)), ((a.head(0),b),a.head(0).merge(b,left_on="kod",right_on="id",how="left")), ((a,b.head(0)),a.merge(b.head(0),left_on="kod",right_on="id",how="left"))]
check_cases(c, ns, 'spoj_jine_nazvy', cases)
c.done()
