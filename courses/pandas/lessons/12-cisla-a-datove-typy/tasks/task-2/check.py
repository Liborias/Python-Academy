import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["12,5","-0,25","3.0",None,"chyba"],index=["E","B","A","D","C"],name="cena",dtype="str")
empty=pd.Series([],name="nic",dtype="str")
extra=pd.Series(["0","1,2345","-2"],name="jine",dtype="str")

cases = [((s,),pd.Series([12.5,-0.25,3.0,None,None],index=s.index,name="cena",dtype="float64")), ((empty,),pd.Series([],index=empty.index,name="nic",dtype="float64")), ((extra,),pd.Series([0.0,1.2345,-2.0],index=extra.index,name="jine",dtype="float64"))]
check_cases(c, ns, 'preved_desetinnou_carku', cases)
c.done()
