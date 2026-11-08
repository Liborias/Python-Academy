import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"misto":["Brno","Praha","Zlín"],"teplota":[18.5,None,-2.0],"vlhkost":[65,58,72]}, index=["B","A","C"])
numeric = pd.DataFrame({"prvni":[1.5,0.0,-2.0],"druhy":[8.0,4.0,3.0]}, index=[20,0,10])

cases = [((df,"A"),df.loc["A"]), ((df,"C"),df.loc["C"]), ((numeric,0),numeric.loc[0])]
check_cases(c, ns, 'vyber_radek', cases)
c.done()
