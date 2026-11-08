import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
a=pd.DataFrame({"kod":["B","A","B"],"mereni":[2.0,3.0,4.0]},index=[4,1,3])
b=pd.DataFrame({"kod":["A","C"],"limit":[10.0,20.0]})

cases = [((a,b,"kod"),pd.DataFrame({"kod":["B","A","B"],"mereni":[2.0,3.0,4.0],"limit":[None,10.0,None]})), ((a.rename(columns={"kod":"id"}),b.rename(columns={"kod":"id"}),"id"),a.rename(columns={"kod":"id"}).merge(b.rename(columns={"kod":"id"}),on="id",how="left")), ((a.head(0),b,"kod"),a.head(0).merge(b,on="kod",how="left"))]
check_cases(c, ns, 'spoj_podle_klice', cases)
c.done()
