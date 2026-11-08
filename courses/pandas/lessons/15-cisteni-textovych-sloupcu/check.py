import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["  PRAHA "," Brno","ŽĎÁR  ","",None,"Straße"],index=["F","B","A","E","D","C"],name="misto",dtype="str")
extra=pd.Series([" A  B "," C\tD "],name="jine",dtype="str")

cases = [((s,),pd.Series(["praha","brno","žďár","",None,"straße"],index=s.index,name=s.name,dtype="str")), ((s.iloc[:0],),s.iloc[:0]), ((extra,),pd.Series(["a  b","c\td"],name="jine",dtype="str"))]
check_cases(c, ns, 'vycisti_text', cases)
c.done()
