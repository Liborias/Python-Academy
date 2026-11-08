import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
s=pd.Series([7,1,4],index=["B","C","A"],name="hodnota",dtype="float64");num=pd.Series([4,1,7],index=[20,30,10],dtype="float64");empty=pd.Series([],dtype="float64")

cases=[((s,),s.sort_index()), ((num,),num.sort_index()), ((empty,),empty)]
check_cases(c,ns,'serad_podle_popisku',cases)
c.done()
