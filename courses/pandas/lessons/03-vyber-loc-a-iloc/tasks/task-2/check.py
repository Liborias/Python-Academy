import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
s=pd.Series([8,6,9,4],index=["C","A","D","B"],name="hodnota",dtype="float64")

cases=[((s,1,3),s.iloc[1:3]), ((s,0,0),s.iloc[0:0]), ((s,-2,9),s.iloc[-2:9])]
check_cases(c,ns,'vyber_usek',cases)
c.done()
