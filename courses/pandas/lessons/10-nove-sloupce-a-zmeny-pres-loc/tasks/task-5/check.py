import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"cena":[12.5,0.0,None,7.0],"kusy":[2,4,3,0],"kod":["B","A","D","C"]}, index=["r2","r0","r3","r1"])
s=pd.Series([8.0,None,6.0,5.0],index=["r1","r3","r0","r2"],name="nove",dtype="float64")
a=df.copy();a["cena"]=[5.0,6.0,None,8.0]

cases = [((df,"cena",s),a), ((df,"cena",s.rename("jiny_nazev")),a), ((df.head(0),"cena",s.iloc[0:0]),df.head(0))]
check_cases(c, ns, 'prepocitej_podle_popisku', cases)
c.done()
