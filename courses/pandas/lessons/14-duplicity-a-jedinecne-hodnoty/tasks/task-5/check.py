import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["B","A","B",None,"C",None],name="misto",dtype="str")
extra=pd.Series([None,"","",None,"X"],index=[5,0,4,1,3],name="jine",dtype="str")

cases = [((s,),s.value_counts(dropna=False,sort=False)), ((s.iloc[:0],),s.iloc[:0].value_counts(dropna=False,sort=False)), ((extra,),extra.value_counts(dropna=False,sort=False))]
check_cases(c, ns, 'pocty_hodnot', cases)
c.done()
