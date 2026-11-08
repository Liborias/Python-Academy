import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["01.02.2026","31.02.2026",None,"29.02.2024","29.02.2026",""],index=["F","B","A","E","D","C"],name="datum",dtype="str")
extra=pd.Series(["text",None],name="jine",dtype="str")

cases = [((s,),pd.Series([False,True,False,False,True,True],index=s.index,name=s.name)), ((s.iloc[:0],),pd.Series([],index=s.index[:0],name=s.name,dtype=bool)), ((extra,),pd.Series([True,False],name="jine"))]
check_cases(c, ns, 'chybne_datumy', cases)
c.done()
