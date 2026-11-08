import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series([None,"A",None,"B",None],index=["E","A","D","B","C"],name="stav",dtype="str")
n=pd.Series([None,0,None,3,None],name="kusy",dtype="Int64")
all_na=pd.Series([None,None],name="mereni",dtype="float64")

cases = [((s,),s.ffill()), ((n,),n.ffill()), ((all_na,),all_na), ((s.iloc[:0],),s.iloc[:0])]
check_cases(c, ns, 'dopln_predchozi', cases)
c.done()
