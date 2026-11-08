import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"A":[1.0,None,0.0,None],"B":[2.0,3.0,None,None],"text":["x","y","z","w"]},index=["D","A","C","B"])
extra=pd.DataFrame({"s":["",None,"X"]})

cases = [((df,["B","A","text"]),pd.Series([2,2,4],index=["B","A","text"],dtype="int64")), ((df.head(0),["A"]),pd.Series([0],index=["A"],dtype="int64")), ((df,[]),pd.Series([],dtype="int64")), ((extra,["s"]),pd.Series([2],index=["s"],dtype="int64"))]
check_cases(c, ns, 'pocet_dostupnych', cases)
c.done()
