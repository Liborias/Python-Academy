import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
a=pd.DataFrame({"kod":["B","A"],"leva":[2.0,1.0]},index=[5,2])
b=pd.DataFrame({"kod":["A","C"],"prava":[10.0,30.0]})

cases = [((a,b,"kod"),a.merge(b,on="kod",how="outer",sort=True,indicator=True)), ((a.head(0),b,"kod"),a.head(0).merge(b,on="kod",how="outer",sort=True,indicator=True)), ((a,b.head(0),"kod"),a.merge(b.head(0),on="kod",how="outer",sort=True,indicator=True))]
check_cases(c, ns, 'pridej_stav_spojeni', cases)
c.done()
