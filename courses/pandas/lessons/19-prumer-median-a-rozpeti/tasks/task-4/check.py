import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"A":[1.0,None,0.0,None],"B":[2.0,3.0,None,None],"text":["x","y","z","w"]},index=["D","A","C","B"])

cases = [((df,["B","A"]),pd.Series([2.5,0.5],index=["B","A"])), ((df.head(0),["A"]),pd.Series([None],index=["A"],dtype="float64")), ((df,[]),pd.Series([],dtype="float64"))]
asym = pd.DataFrame({"A":[1.0,1.0,100.0],"B":[2.0,3.0,4.0]})
cases.append(((asym,["A","B"]),pd.Series([1.0,3.0],index=["A","B"])))
check_cases(c, ns, 'mediany_sloupcu', cases)
c.done()
