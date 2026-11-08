import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"teplota":[0.0,None,3.5,None],"misto":["Brno","",None,"Praha"],"kusy":pd.array([0,2,None,1],dtype="Int64")},index=["C","A","D","B"])

cases = [((df,),pd.Series([2,1,1],index=df.columns,dtype="int64")), ((df.head(0),),pd.Series(0,index=df.columns,dtype="int64")), ((pd.DataFrame(index=["X","Y"]),),pd.Series([],dtype="int64"))]
check_cases(c, ns, 'chybejici_pocty', cases)
c.done()
