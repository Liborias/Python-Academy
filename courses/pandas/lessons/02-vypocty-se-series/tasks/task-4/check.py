import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
s=pd.Series([10,None,20,-5],index=["C","A","B","D"],name="mereni",dtype="float64");empty=pd.Series([],dtype="float64",name="mereni")

cases=[((s,),s-s.mean()), ((s*0,),s*0), ((empty,),empty)]
check_cases(c,ns,'odchylky_od_prumeru',cases)
c.done()
