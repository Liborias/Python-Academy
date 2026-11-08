import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
idx=pd.DatetimeIndex(["2026-02-01 00:00:00","2026-02-01 08:00:00","2026-02-01 23:59:59.999999","2026-02-02 00:00:00"],name="cas").as_unit("us")
df=pd.DataFrame({"hodnota":[1.0,2.0,3.0,4.0],"misto":["A","B","C","D"]},index=idx)

cases = [((df,),df.reset_index()), ((df.iloc[::-1],),df.iloc[::-1].reset_index()), ((df.head(0),),df.head(0).reset_index()), ((df[[]],),df[[]].reset_index())]
check_cases(c, ns, 'cas_zpet_do_sloupce', cases)
c.done()
