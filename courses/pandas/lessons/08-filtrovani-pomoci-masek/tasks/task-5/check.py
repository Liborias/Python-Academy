import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"teplota":[10.0,20.0,None,30.0,-5.0],"vlhkost":[80.0,60.0,90.0,None,45.0],"misto":["Brno","Praha","Brno","Zlín","Praha"]}, index=["C","A","E","B","D"])

cases = [((df,pd.Series([True,False,False,True,False],index=["D","B","E","C","A"],dtype=bool)),df.loc[["C","D"]]), ((df,pd.Series(False,index=df.index)),df.iloc[0:0]), ((df,pd.Series(True,index=df.index)),df), ((df.head(0),pd.Series([],index=df.index[:0],dtype=bool)),df.head(0))]
check_cases(c, ns, 'vyber_podle_masky', cases)
c.done()
