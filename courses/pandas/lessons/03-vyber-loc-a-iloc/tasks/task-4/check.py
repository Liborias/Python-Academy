import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
s=pd.Series([4,7,1],index=["B","C","A"],name="hodnota",dtype="float64")

cases=[((s,{"A":"Brno"}),s.rename(index={"A":"Brno"})), ((s,{}),s), ((s,{"A":"B"}),s.rename(index={"A":"B"}))]
check_cases(c,ns,'prejmenuj_popisky',cases)
c.done()
