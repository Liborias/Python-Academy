import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
s=pd.Series([0.0,3.0],index=pd.DatetimeIndex(["2026-02-01","2026-02-03"],name="den").as_unit("us"),name="mereni",dtype="float64")

cases = [((s,"2026-02-01","2026-02-03"),pd.Series([0.0,None,3.0],index=pd.date_range("2026-02-01","2026-02-03",freq="D",name="den").as_unit("us"),name="mereni")), ((s,"2026-01-31","2026-02-02"),s.reindex(pd.date_range("2026-01-31","2026-02-02",freq="D",name="den").as_unit("us"))), ((s.iloc[:0],"2026-02-01","2026-02-03"),s.iloc[:0].reindex(pd.date_range("2026-02-01","2026-02-03",freq="D",name="den").as_unit("us"))), ((s.rename("X").rename_axis(None),"2026-02-01","2026-02-01"),s.rename("X").rename_axis(None).reindex(pd.date_range("2026-02-01","2026-02-01",freq="D").as_unit("us")))]
check_cases(c, ns, 'pravidelna_mrizka', cases)
c.done()
