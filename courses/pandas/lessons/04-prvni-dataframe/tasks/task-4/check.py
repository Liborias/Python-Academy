import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
df=pd.DataFrame({"misto":["Brno","Praha","Zlin"],"hodnota":[2.5,None,0]},index=["B","A","C"]);empty=df.head(0)

cases=[((df,2),df.head(2)), ((df,0),df.head(0)), ((df,20),df), ((empty,2),empty)]
check_cases(c,ns,'prvni_radky',cases)
c.done()
