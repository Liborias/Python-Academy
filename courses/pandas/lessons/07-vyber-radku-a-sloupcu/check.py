import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"misto":["Brno","Praha","Zlín"],"teplota":[18.5,None,-2.0],"vlhkost":[65,58,72]}, index=["B","A","C"])
numeric = pd.DataFrame({"prvni":[1.5,0.0,-2.0],"druhy":[8.0,4.0,3.0]}, index=[20,0,10])

cases = [((df,["C","B"],["vlhkost","misto"]),df.loc[["C","B"],["vlhkost","misto"]]), ((df,[],["misto"]),df.loc[[],["misto"]]), ((df,["A","A"],[]),df.loc[["A","A"],[]]), ((numeric,[0,20],["druhy"]),numeric.loc[[0,20],["druhy"]])]
check_cases(c, ns, 'vyber_obdelnik', cases)
c.done()
