import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
s=pd.Series([0,None,-4],index=["C","A","B"],name="body",dtype="float64");empty=pd.Series([],dtype="float64",name="body")

cases=[((s,3),s+3), ((s,-2.5),s-2.5), ((empty,9),empty)]
check_cases(c,ns,'pricti_bonus',cases)
c.done()
