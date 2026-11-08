import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases, equivalent

c = check()
ns = c.load()
df=pd.DataFrame({"cas":pd.array(["2026-02-02 00:00:00","2026-02-01 08:00:00","2026-02-01 08:00:00","2026-02-01 23:59:59.999999"],dtype="datetime64[us]"),"hodnota":[2.0,1.0,3.0,4.0],"misto":["B","A","C","D"]},index=["r3","r1","r2","r0"])

cases = [((df,"cas"),df.iloc[[1,2,3,0]].set_index("cas")), ((df.head(0),"cas"),df.head(0).set_index("cas")), ((df.rename(columns={"cas":"datum"}),"datum"),df.rename(columns={"cas":"datum"}).iloc[[1,2,3,0]].set_index("datum"))]
many = pd.DataFrame({"cas":pd.array([pd.Timestamp("2026-02-01") + pd.Timedelta(minutes=k % 4) for k in range(40)],dtype="datetime64[us]"),"poradi":range(40)})
cases.append(((many,"cas"),many.set_index("cas").sort_index(kind="stable")))
check_cases(c, ns, 'nastav_casovy_index', cases)
c.done()
