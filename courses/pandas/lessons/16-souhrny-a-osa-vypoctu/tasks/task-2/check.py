import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"A":[1.0,None,0.0,None],"B":[2.0,3.0,None,None],"text":["x","y","z","w"]},index=["D","A","C","B"])

cases = [((df,["A","B"]),pd.Series([3.0,3.0,0.0,None],index=df.index)), ((df,[]),pd.Series(float("nan"),index=df.index)), ((df.head(0),["B"]),pd.Series([],index=df.index[:0],dtype="float64"))]
check_cases(c, ns, 'soucty_radku', cases)
c.done()
