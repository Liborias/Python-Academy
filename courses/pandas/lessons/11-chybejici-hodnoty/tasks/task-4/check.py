import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"teplota":[0.0,None,3.5,None],"misto":["Brno","",None,"Praha"],"kusy":pd.array([0,2,None,1],dtype="Int64")},index=["C","A","D","B"])

cases = [((df,["misto","teplota"]),pd.Series([False,True,True,True],index=df.index)), ((df,["misto"]),pd.Series([False,False,True,False],index=df.index)), ((df,[]),pd.Series(False,index=df.index)), ((df.head(0),["misto"]),pd.Series([],index=df.index[:0],dtype=bool))]
check_cases(c, ns, 'chybi_na_radku', cases)
c.done()
