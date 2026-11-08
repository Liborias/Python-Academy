import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["01.02.2026","31.02.2026",None,"29.02.2024","29.02.2026",""],index=["F","B","A","E","D","C"],name="datum",dtype="str")
extra=pd.Series(["31.12.2025","02.01.2026"],name="jine",dtype="str")

cases = [((s,),pd.Series([pd.Timestamp("2026-02-01"),pd.NaT,pd.NaT,pd.Timestamp("2024-02-29"),pd.NaT,pd.NaT],index=s.index,name=s.name,dtype="datetime64[us]")), ((s.iloc[:0],),pd.Series([],index=s.index[:0],name=s.name,dtype="datetime64[us]")), ((extra,),pd.Series([pd.Timestamp("2025-12-31"),pd.Timestamp("2026-01-02")],name="jine",dtype="datetime64[us]"))]
check_cases(c, ns, 'preved_data', cases)
c.done()
