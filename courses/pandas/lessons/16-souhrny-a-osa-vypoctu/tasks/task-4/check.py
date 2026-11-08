import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"A":[1.0,None,0.0,None],"B":[2.0,3.0,None,None],"text":["x","y","z","w"]},index=["D","A","C","B"])

cases = [((df,),{"radky":4,"bunky":12}), ((df.head(0),),{"radky":0,"bunky":0}), ((pd.DataFrame(index=["B","A"]),),{"radky":2,"bunky":0})]
check_cases(c, ns, 'rozsah_tabulky', cases)
c.done()
