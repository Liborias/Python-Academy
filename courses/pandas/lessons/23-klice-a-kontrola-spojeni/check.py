import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
prodeje=pd.DataFrame({"produkt":["B","A","B","X"],"kusy":[1,2,3,0]},index=["z","a","y","b"])
cenik=pd.DataFrame({"produkt":["A","B","C"],"cena":[10.0,20.0,None]})
bad=pd.concat([cenik,cenik.iloc[[0]]],ignore_index=True)
unused=pd.concat([cenik,cenik.iloc[[2]]],ignore_index=True)

cases = [((prodeje,cenik),prodeje.merge(cenik,on="produkt",how="left",sort=False)), ((prodeje.head(0),cenik),prodeje.head(0).merge(cenik,on="produkt",how="left")), ((prodeje,cenik.head(0)),prodeje.merge(cenik.head(0),on="produkt",how="left"))]
check_cases(c, ns, 'overene_ceny', cases)
from copy import deepcopy
for args in [(prodeje,bad),(prodeje,unused)]:
    values=deepcopy(args)
    before=deepcopy(values)
    c.raises(ns, 'overene_ceny', values, pd.errors.MergeError)
    c.add("Zachování vstupů při odmítnutí", equivalent(values,before,exact=True), "Neplatné klíče odmítněte bez úpravy zdrojových tabulek.")
c.done()
