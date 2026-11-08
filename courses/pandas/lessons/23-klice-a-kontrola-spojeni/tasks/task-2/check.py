import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
a=pd.DataFrame({"kod":["B","A"],"leva":[2.0,1.0]},index=[5,2])
b=pd.DataFrame({"kod":["A","C"],"prava":[10.0,30.0]})
bad_a=pd.concat([a,a.iloc[[0]]],ignore_index=True)
bad_b=pd.concat([b,b.iloc[[0]]],ignore_index=True)

cases = [((a,b,"kod"),pd.DataFrame({"kod":["A","B","C"],"leva":[1.0,2.0,None],"prava":[10.0,None,30.0]})), ((a.head(0),b,"kod"),a.head(0).merge(b,on="kod",how="outer",sort=True)), ((a.rename(columns={"kod":"id"}),b.rename(columns={"kod":"id"}),"id"),a.rename(columns={"kod":"id"}).merge(b.rename(columns={"kod":"id"}),on="id",how="outer",sort=True))]
check_cases(c, ns, 'spoj_jednoznacne', cases)
from copy import deepcopy
for args in [(bad_a,b,"kod"),(a,bad_b,"kod"),(bad_a,bad_b,"kod")]:
    values=deepcopy(args)
    before=deepcopy(values)
    c.raises(ns, 'spoj_jednoznacne', values, pd.errors.MergeError)
    c.add("Zachování vstupů při odmítnutí", equivalent(values,before,exact=True), "Neplatné klíče odmítněte bez úpravy zdrojových tabulek.")
c.done()
