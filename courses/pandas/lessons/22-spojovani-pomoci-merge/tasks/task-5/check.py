import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
a=pd.DataFrame({"den":["2026-02-02","2026-02-01","2026-02-02"],"produkt":["A","A","X"],"kusy":[1,3,2]},index=[3,0,2])
b=pd.DataFrame({"den":["2026-02-01","2026-02-02"],"produkt":["A","A"],"cena":[10.0,11.0]})

cases = [((a,b),pd.DataFrame({"den":["2026-02-02","2026-02-01","2026-02-02"],"produkt":["A","A","X"],"kusy":[1,3,2],"cena":[11.0,10.0,None]})), ((a.head(0),b),a.head(0).merge(b,on=["den","produkt"],how="left")), ((a,b.head(0)),a.merge(b.head(0),on=["den","produkt"],how="left"))]
check_cases(c, ns, 'spoj_dva_klice', cases)
c.done()
