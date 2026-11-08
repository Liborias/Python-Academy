import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
a=pd.Series([10,25],index=["B","A"],dtype="float64");b=pd.Series([3,2],index=["A","B"],dtype="float64");empty=pd.Series([],dtype="float64")

cases=[((a,b),(a*b).sort_index().rename("trzba")), ((a,b*0),(a*(b*0)).sort_index().rename("trzba")), ((empty,empty),empty.rename("trzba"))]
check_cases(c,ns,'celkove_trzby',cases)
c.done()
