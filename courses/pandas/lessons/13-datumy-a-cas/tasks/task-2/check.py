import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["2026-02-01 08:30","2026-02-01 25:00",None,"2025-12-31 23:59","2026-02-31 10:00"],index=["E","B","A","D","C"],name="cas",dtype="str")
extra=pd.Series(["2024-02-29 00:00"],name="jine",dtype="str")

cases = [((s,),pd.Series([pd.Timestamp("2026-02-01 08:30"),pd.NaT,pd.NaT,pd.Timestamp("2025-12-31 23:59"),pd.NaT],index=s.index,name=s.name,dtype="datetime64[us]")), ((s.iloc[:0],),pd.Series([],index=s.index[:0],name=s.name,dtype="datetime64[us]")), ((extra,),pd.Series([pd.Timestamp("2024-02-29 00:00")],name="jine",dtype="datetime64[us]"))]
check_cases(c, ns, 'preved_casy', cases)
c.done()
