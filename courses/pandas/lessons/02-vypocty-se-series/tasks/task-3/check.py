import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
s=pd.Series([10,None,20],dtype="float64");empty=pd.Series([],dtype="float64")

cases=[((s,),{"soucet":30.0,"prumer":15.0}), ((empty,),{"soucet":0.0,"prumer":float("nan")}), ((s*0,),{"soucet":0.0,"prumer":0.0})]
check_cases(c,ns,'souhrn_hodnot',cases)
c.done()
