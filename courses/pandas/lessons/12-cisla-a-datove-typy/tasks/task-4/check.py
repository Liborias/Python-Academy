import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"kusy":["2",None,"0"],"cena":["12.5","0","3.0"],"kod":["001","007","010"]},index=["C","A","B"])
extra=pd.DataFrame({"cislo":[0,3],"text":["A","B"]})

cases = [((df,{"kusy":"Int64","cena":"float64"}),df.astype({"kusy":"Int64","cena":"float64"})), ((df,{}),df), ((df.head(0),{"kusy":"Int64"}),df.head(0).astype({"kusy":"Int64"})), ((extra,{"cislo":"str"}),extra.astype({"cislo":"str"}))]
check_cases(c, ns, 'preved_sloupce', cases)
c.done()
