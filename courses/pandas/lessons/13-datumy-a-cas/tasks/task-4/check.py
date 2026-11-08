import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"datum":pd.array([pd.Timestamp("2026-02-01"),pd.Timestamp("2026-02-02"),pd.NaT,pd.Timestamp("2026-01-31")],dtype="datetime64[us]"),"kusy":[3,5,2,0]},index=["B","A","C","D"])

cases = [((df,"datum","2026-02-01","2026-02-02"),df.loc[["B","A"]]), ((df,"datum","2026-02-02","2026-02-02"),df.loc[["A"]]), ((df,"datum","2030-01-01","2030-01-02"),df.head(0)), ((df.head(0),"datum","2026-01-01","2026-12-31"),df.head(0)), ((df.rename(columns={"datum":"den"}),"den","2026-01-31","2026-02-01"),df.rename(columns={"datum":"den"}).loc[["B","D"]])]
check_cases(c, ns, 'vyber_obdobi', cases)
c.done()
