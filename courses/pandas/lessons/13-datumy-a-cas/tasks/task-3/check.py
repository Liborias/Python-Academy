import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series([pd.Timestamp("2026-02-01"),pd.NaT,pd.Timestamp("2024-02-29")],index=["C","A","B"],name="datum",dtype="datetime64[us]")
extra=pd.Series([pd.Timestamp("1999-12-31"),pd.Timestamp("2000-01-01")],name="jine",dtype="datetime64[us]")

cases = [((s,),pd.Series([2026,None,2024],index=s.index,name=s.name,dtype="Int64")), ((s.iloc[:0],),pd.Series([],index=s.index[:0],name=s.name,dtype="Int64")), ((extra,),pd.Series([1999,2000],name="jine",dtype="Int64"))]
check_cases(c, ns, 'rok_z_data', cases)
c.done()
