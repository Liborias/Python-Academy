import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"misto":["Brno","Praha","Zlín"],"teplota":[18.5,None,-2.0],"vlhkost":[65,58,72]}, index=["B","A","C"])

cases = [((df,{"teplota":"teplota_c"}),df.rename(columns={"teplota":"teplota_c"})), ((df,{}),df), ((df.head(0),{"misto":"stanice","vlhkost":"procenta"}),df.head(0).rename(columns={"misto":"stanice","vlhkost":"procenta"}))]
check_cases(c, ns, 'prejmenuj_sloupce', cases)
c.done()
