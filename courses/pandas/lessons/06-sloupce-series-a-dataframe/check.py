import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"misto":["Brno","Praha","Zlín"],"teplota":[18.5,None,-2.0],"vlhkost":[65,58,72]}, index=["B","A","C"])

cases = [((df,"teplota"),df["teplota"]), ((df,"misto"),df["misto"]), ((df.head(0),"vlhkost"),df["vlhkost"].head(0))]
check_cases(c, ns, 'vyber_sloupec', cases)
c.done()
