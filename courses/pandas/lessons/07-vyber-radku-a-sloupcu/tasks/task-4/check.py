import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"misto":["Brno","Praha","Zlín"],"teplota":[18.5,None,-2.0],"vlhkost":[65,58,72]}, index=["B","A","C"])
numeric = pd.DataFrame({"prvni":[1.5,0.0,-2.0],"druhy":[8.0,4.0,3.0]}, index=[20,0,10])

cases = [((df,[2,0]),df.iloc[[2,0]]), ((df,[-1,0,-1]),df.iloc[[-1,0,-1]]), ((df,[]),df.iloc[[]]), ((numeric,[1,0]),numeric.iloc[[1,0]])]
check_cases(c, ns, 'vyber_radky_pozicemi', cases)
c.done()
