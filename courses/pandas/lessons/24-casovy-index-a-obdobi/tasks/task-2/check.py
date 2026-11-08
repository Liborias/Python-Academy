import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
idx=pd.DatetimeIndex(["2026-02-01 00:00:00","2026-02-01 08:00:00","2026-02-01 23:59:59.999999","2026-02-02 00:00:00"],name="cas").as_unit("us")
df=pd.DataFrame({"hodnota":[1.0,2.0,3.0,4.0],"misto":["A","B","C","D"]},index=idx)
duplicated=pd.concat([df,df.iloc[[1]]]).sort_index(kind="stable")

cases = [((df,"2026-02-01 00:00:00","2026-02-01 08:00:00"),df.iloc[:2]), ((df,"2026-02-01 08:00:00","2026-02-01 08:00:00"),df.iloc[1:2]), ((df,"2030-01-01 00:00:00","2030-01-02 00:00:00"),df.head(0)), ((df.head(0),"2026-02-01 00:00:00","2026-02-02 00:00:00"),df.head(0)), ((duplicated,"2026-02-01 08:00:00","2026-02-01 08:00:00"),duplicated.loc[[pd.Timestamp("2026-02-01 08:00:00")]])]
check_cases(c, ns, 'casovy_usek', cases)
c.done()
