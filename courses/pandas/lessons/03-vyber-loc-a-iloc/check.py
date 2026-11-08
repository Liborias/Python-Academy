import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
s=pd.Series([4,7,1],index=["B","C","A"],name="hodnota",dtype="float64");integer=pd.Series([1,2,3],index=[10,20,30],name="cisla",dtype="float64")

cases=[((s,["C","A"]),s.loc[["C","A"]]), ((s,[]),s.loc[[]]), ((s,["B","B"]),s.loc[["B","B"]]), ((integer,[20,10]),integer.loc[[20,10]])]
check_cases(c,ns,'vyber_podle_popisku',cases)
c.done()
