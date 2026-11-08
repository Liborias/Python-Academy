import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"teplota":[0.0,None,3.5,None],"misto":["Brno","",None,"Praha"],"kusy":pd.array([0,2,None,1],dtype="Int64")},index=["C","A","D","B"])

cases = [((df,{"teplota":-1.0,"misto":"nezname","kusy":0}),df.fillna({"teplota":-1.0,"misto":"nezname","kusy":0})), ((df,{"misto":"X"}),df.fillna({"misto":"X"})), ((df,{}),df), ((df.head(0),{"teplota":0.0}),df.head(0))]
check_cases(c, ns, 'dopln_hodnoty', cases)
c.done()
