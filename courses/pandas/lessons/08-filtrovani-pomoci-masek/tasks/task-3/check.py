import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"teplota":[10.0,20.0,None,30.0,-5.0],"vlhkost":[80.0,60.0,90.0,None,45.0],"misto":["Brno","Praha","Brno","Zlín","Praha"]}, index=["C","A","E","B","D"])

cases = [((df,"teplota",20,"vlhkost",80),df.loc[["C","A","E","B"]]), ((df,"teplota",10,"vlhkost",60),df.loc[["C","A","E","B"]]), ((df,"vlhkost",100,"teplota",100),df.iloc[0:0]), ((df.head(0),"teplota",0,"vlhkost",0),df.head(0))]
check_cases(c, ns, 'vyber_nekterou_podminku', cases)
c.done()
