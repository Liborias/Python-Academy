import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series([10.0,10.0,12.0,1000.0,None],index=["E","A","D","B","C"],name="mereni",dtype="float64")
empty=s.iloc[:0]
all_na=pd.Series([None,None],dtype="float64")

cases = [((s,),990.0), ((empty,),float("nan")), ((all_na,),float("nan")), ((pd.Series([-5.0,2.0],dtype="float64"),),7.0), ((pd.Series([3.0,None],dtype="float64"),),0.0)]
check_cases(c, ns, 'rozpeti_hodnot', cases)
c.done()
