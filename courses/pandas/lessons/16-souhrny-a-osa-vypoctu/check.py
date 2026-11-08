import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"A":[1.0,None,0.0,None],"B":[2.0,3.0,None,None],"text":["x","y","z","w"]},index=["D","A","C","B"])

cases = [((df,["B","A"]),pd.Series([5.0,1.0],index=["B","A"],dtype="float64")), ((df.head(0),["A"]),pd.Series([None],index=["A"],dtype="float64")), ((df,[]),pd.Series([],dtype="float64"))]
check_cases(c, ns, 'soucty_sloupcu', cases)
c.done()
