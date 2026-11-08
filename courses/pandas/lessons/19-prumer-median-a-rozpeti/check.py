import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series([10.0,10.0,12.0,1000.0,None],index=["E","A","D","B","C"],name="mereni",dtype="float64")
empty=s.iloc[:0]
all_na=pd.Series([None,None],dtype="float64")
unknown={"dostupne":0,"minimum":float("nan"),"maximum":float("nan"),"prumer":float("nan"),"median":float("nan")}
negative=pd.Series([-10.0,-1.0,5.0],dtype="float64")

cases = [((s,),{"dostupne":4,"minimum":10.0,"maximum":1000.0,"prumer":258.0,"median":11.0}), ((empty,),unknown), ((all_na,),unknown), ((negative,),{"dostupne":3,"minimum":-10.0,"maximum":5.0,"prumer":-2.0,"median":-1.0})]
check_cases(c, ns, 'popis_hodnot', cases)
c.done()
