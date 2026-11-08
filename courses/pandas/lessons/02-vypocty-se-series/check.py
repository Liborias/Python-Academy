import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
s=pd.Series([50,0,-12.5,None],index=["C","A","B","D"],name="cena",dtype="float64")

cases=[((s,25),s/25), ((s,3),s/3), ((s,2.5),s/2.5), ((pd.Series([],dtype="float64",name="cena"),3),pd.Series([],dtype="float64",name="cena"))]
check_cases(c,ns,'preved_na_eura',cases)
c.done()
