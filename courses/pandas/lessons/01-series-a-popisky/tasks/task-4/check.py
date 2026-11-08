import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()

cases=[((pd.Series([5,0,-2],index=["C","A","B"],dtype="float64"),),[5.0,0.0,-2.0]), ((pd.Series([],dtype="float64"),),[]), ((pd.Series([None,2],dtype="float64"),),[float("nan"),2.0])]
check_cases(c,ns,'seznam_hodnot',cases)
c.done()
