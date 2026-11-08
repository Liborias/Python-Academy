import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
s=pd.Series([8,6,9],index=[10,20,30],name="hodnota",dtype="float64")

cases=[((s,[2,0]),s.iloc[[2,0]]), ((s,[-1,0,-1]),s.iloc[[-1,0,-1]]), ((s,[]),s.iloc[[]])]
check_cases(c,ns,'vyber_pozice',cases)
c.done()
