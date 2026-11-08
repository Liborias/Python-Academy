import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
idx=pd.DatetimeIndex(["2026-02-01 08:00","2026-02-01 08:00","2026-02-01 12:00","2026-02-03 00:00","2026-02-04 00:00","2026-02-04 23:59"],name="cas").as_unit("us")
s=pd.Series([1.0,2.0,None,0.0,None,None],index=idx,name="mereni",dtype="float64")
days=pd.date_range("2026-02-01","2026-02-04",freq="D",name="cas").as_unit("us")
df=s.to_frame();df["misto"]=["A","B","C","D","E","F"]

cases = [((df,"mereni"),pd.DataFrame({"radky":[3,0,1,2],"dostupne":[2,0,1,0],"prumer":[1.5,None,0.0,None]},index=days)), ((df.head(0),"mereni"),df.head(0).resample("D").agg(radky=("mereni","size"),dostupne=("mereni","count"),prumer=("mereni","mean"))), ((df.rename(columns={"mereni":"hodnota"}),"hodnota"),pd.DataFrame({"radky":[3,0,1,2],"dostupne":[2,0,1,0],"prumer":[1.5,None,0.0,None]},index=days))]
check_cases(c, ns, 'denni_prehled', cases)
c.done()
