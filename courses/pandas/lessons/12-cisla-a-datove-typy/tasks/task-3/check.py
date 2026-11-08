import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series([2.0,None,0.0,-1.0],index=["D","A","C","B"],name="kusy",dtype="float64")
other=pd.Series([None,4],name="jine",dtype="Int64")

cases = [((s,),pd.Series([2,None,0,-1],index=s.index,name="kusy",dtype="Int64")), ((s.iloc[:0],),s.iloc[:0].astype("Int64")), ((other,),other)]
check_cases(c, ns, 'cele_pocty', cases)
c.done()
