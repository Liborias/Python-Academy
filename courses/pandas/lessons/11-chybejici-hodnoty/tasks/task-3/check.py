import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"teplota":[0.0,None,3.5,None],"misto":["Brno","",None,"Praha"],"kusy":pd.array([0,2,None,1],dtype="Int64")},index=["C","A","D","B"])

cases = [((df,["misto"]),df.loc[["C","A","B"]]), ((df,["teplota","kusy"]),df.loc[["C"]]), ((df,[]),df), ((df.head(0),["misto"]),df.head(0))]
check_cases(c, ns, 'odstran_neuplne', cases)
c.done()
