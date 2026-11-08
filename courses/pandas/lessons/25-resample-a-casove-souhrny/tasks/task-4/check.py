import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
s=pd.Series([2.0,3.0,4.0,None],index=pd.DatetimeIndex(["2026-01-31 23:59:59.999999","2026-02-01 00:00","2026-02-28 12:00","2026-04-01 00:00"],name="cas").as_unit("us"),name="mereni",dtype="float64")
leap=pd.Series([1.0,2.0],index=pd.DatetimeIndex(["2024-02-29 23:59:59.999999","2024-03-01 00:00"],name="datum").as_unit("us"),name="X",dtype="float64")

cases = [((s,),pd.Series([2.0,7.0,None,None],index=pd.date_range("2026-01-01","2026-04-01",freq="MS",name="cas").as_unit("us"),name="mereni")), ((s.iloc[:0],),s.iloc[:0].resample("MS").sum(min_count=1)), ((leap,),pd.Series([1.0,2.0],index=pd.date_range("2024-02-01","2024-03-01",freq="MS",name="datum").as_unit("us"),name="X"))]
check_cases(c, ns, 'mesicni_soucty', cases)
c.done()
