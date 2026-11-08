import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"cena":[12.5,0.0,None,7.0],"kusy":[2,4,3,0],"kod":["B","A","D","C"]}, index=["r2","r0","r3","r1"])

cases = [((df,"cena","eura",3),df.assign(eura=df["cena"]/3)), ((df,"kusy","novy pocet",2.5),df.assign(**{"novy pocet":df["kusy"]/2.5})), ((df.head(0),"cena","eura",25),df.head(0).assign(eura=df["cena"].head(0)/25))]
check_cases(c, ns, 'pridej_prevod', cases)
c.done()
