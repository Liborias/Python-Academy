import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
prodeje=pd.DataFrame({"produkt":["B","A","B","X"],"kusy":[1,2,3,0]},index=["z","a","y","b"])
cenik=pd.DataFrame({"produkt":["A","B","C"],"cena":[10.0,20.0,None]})

cases = [((prodeje,cenik),pd.DataFrame({"produkt":["B","A","B","X"],"kusy":[1,2,3,0],"cena":[20.0,10.0,20.0,None]})), ((prodeje.head(0),cenik),prodeje.head(0).merge(cenik,on="produkt",how="left")), ((prodeje,cenik.head(0)),prodeje.merge(cenik.head(0),on="produkt",how="left"))]
check_cases(c, ns, 'pripoj_cenik', cases)
c.done()
