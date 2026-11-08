import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"misto":["Brno","Praha","Zlín"],"teplota":[18.5,None,-2.0],"vlhkost":[65,58,72]}, index=["B","A","C"])

cases = [((df,0,2,1,3),df.iloc[0:2,1:3]), ((df,-2,99,-2,99),df.iloc[-2:99,-2:99]), ((df,2,1,0,2),df.iloc[2:1,0:2]), ((df,0,3,2,1),df.iloc[0:3,2:1])]
check_cases(c, ns, 'vyber_pozicovy_blok', cases)
c.done()
