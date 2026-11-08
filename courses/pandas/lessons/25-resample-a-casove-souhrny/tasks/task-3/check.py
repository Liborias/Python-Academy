import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
idx=pd.DatetimeIndex(["2026-02-01 08:00","2026-02-01 08:00","2026-02-01 12:00","2026-02-03 00:00","2026-02-04 00:00","2026-02-04 23:59"],name="cas").as_unit("us")
s=pd.Series([1.0,2.0,None,0.0,None,None],index=idx,name="mereni",dtype="float64")
days=pd.date_range("2026-02-01","2026-02-04",freq="D",name="cas").as_unit("us")

cases = [((s,),pd.Series([1.5,None,0.0,None],index=days,name="mereni",dtype="float64")), ((s.iloc[:0],),s.iloc[:0].resample("D").mean()), ((s.rename("X"),),s.rename("X").resample("D").mean())]
check_cases(c, ns, 'denni_prumery', cases)
c.done()
