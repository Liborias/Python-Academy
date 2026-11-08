import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series([0.0,None,12.0],name="mereni",dtype="float64")
all_na=pd.Series([None,None],dtype="float64")
negative=pd.Series([-5.0,3.0],dtype="float64")

cases = [((s,),{"zaznamy":3,"dostupne":2,"soucet":12.0,"prumer":6.0}), ((s.iloc[:0],),{"zaznamy":0,"dostupne":0,"soucet":float("nan"),"prumer":float("nan")}), ((all_na,),{"zaznamy":2,"dostupne":0,"soucet":float("nan"),"prumer":float("nan")}), ((negative,),{"zaznamy":2,"dostupne":2,"soucet":-2.0,"prumer":-1.0})]
check_cases(c, ns, 'souhrn_mereni', cases)
c.done()
