import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["12.5","chyba",None,"0","-3","2,5",""],index=["G","B","A","F","C","E","D"],name="cena",dtype="str")
empty=pd.Series([],name="nic",dtype="str")
other=pd.Series(["1.25","-0.5","100"],index=[20,0,10],name="mnozstvi",dtype="str")

cases = [((s,),pd.Series([12.5,None,None,0.0,-3.0,None,None],index=s.index,name=s.name,dtype="float64")), ((empty,),pd.Series([],index=empty.index,name="nic",dtype="float64")), ((other,),pd.Series([1.25,-0.5,100.0],index=other.index,name="mnozstvi",dtype="float64"))]
check_cases(c, ns, 'preved_cisla', cases)
c.done()
