import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["12.5","chyba",None,"0","-3","2,5",""],index=["G","B","A","F","C","E","D"],name="cena",dtype="str")
extra=pd.Series([None,"0","x"],index=[2,0,1],name="jine",dtype="str")

cases = [((s,),pd.Series([False,True,False,False,False,True,True],index=s.index,name=s.name)), ((s.iloc[:0],),pd.Series([],index=s.index[:0],name=s.name,dtype=bool)), ((extra,),pd.Series([False,False,True],index=extra.index,name=extra.name))]
check_cases(c, ns, 'chybne_ciselne_vstupy', cases)
c.done()
