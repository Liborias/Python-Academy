import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()

cases=[((pd.Series([5,None,8],dtype="float64"),),3), ((pd.Series([],dtype="float64"),),0), ((pd.Series([None],dtype="float64"),),1)]
check_cases(c,ns,'pocet_mereni',cases)
c.done()
