import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
s=pd.Series([3,None,-1],index=["C","A","B"],name="puvodni",dtype="float64")

cases=[((s,"novy"),s.rename("novy")), ((pd.Series([],dtype="float64",name="A"),"B"),pd.Series([],dtype="float64",name="B"))]
check_cases(c,ns,'prejmenuj_mereni',cases)
c.done()
