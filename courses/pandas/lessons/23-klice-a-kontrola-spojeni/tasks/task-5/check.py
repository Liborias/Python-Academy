import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
a=pd.DataFrame({"kod":["B","A"],"stav":["nova","zaplacena"]},index=[3,0])
b=pd.DataFrame({"kod":["A"],"stav":["skladem"]})

cases = [((a,b,"kod"),pd.DataFrame({"kod":["B","A"],"stav_objednavka":["nova","zaplacena"],"stav_sklad":[None,"skladem"]})), ((a.head(0),b,"kod"),a.head(0).merge(b,on="kod",how="left",suffixes=("_objednavka","_sklad"))), ((a.rename(columns={"kod":"id"}),b.rename(columns={"kod":"id"}),"id"),a.rename(columns={"kod":"id"}).merge(b.rename(columns={"kod":"id"}),on="id",how="left",suffixes=("_objednavka","_sklad")))]
check_cases(c, ns, 'spoj_stejna_jmena', cases)
c.done()
