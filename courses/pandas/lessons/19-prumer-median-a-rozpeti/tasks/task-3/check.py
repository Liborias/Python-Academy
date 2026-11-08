import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series([10.0,10.0,12.0,1000.0,None],index=["E","A","D","B","C"],name="mereni",dtype="float64")
empty=s.iloc[:0]
all_na=pd.Series([None,None],dtype="float64")
same=pd.Series([4.0,4.0,None],name="shoda",dtype="float64")
negative=pd.Series([-5.0,-2.0,1.0],name="jine",dtype="float64")

cases = [((s,),s.loc[["B"]]), ((empty,),empty), ((all_na,),all_na.iloc[:0]), ((same,),same.iloc[:0]), ((negative,),negative.iloc[[2]])]
check_cases(c, ns, 'vyber_nad_prumerem', cases)
c.done()
