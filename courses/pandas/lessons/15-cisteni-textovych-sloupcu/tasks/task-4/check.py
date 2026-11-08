import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["  PRAHA "," Brno","ŽĎÁR  ","",None,"Straße"],index=["F","B","A","E","D","C"],name="misto",dtype="str")
extra=pd.Series(["   ","\t"," A  B "],name="jine",dtype="str")

cases = [((s,),pd.Series(["PRAHA","Brno","ŽĎÁR",None,None,"Straße"],index=s.index,name=s.name,dtype="str")), ((extra,),pd.Series([None,None,"A  B"],index=extra.index,name=extra.name,dtype="str")), ((s.iloc[:0],),s.iloc[:0])]
check_cases(c, ns, 'prazdne_na_chybejici', cases)
c.done()
