import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df = pd.DataFrame({"cena":[12.5,0.0,None,7.0],"kusy":[2,4,3,0],"kod":["B","A","D","C"]}, index=["r2","r0","r3","r1"])
jine = pd.DataFrame({"kusy":[3.0,0.0],"cena":[2.25,10.0]},index=[20,10])

cases = [((df,),df.assign(trzba=df["cena"]*df["kusy"])), ((df.head(0),),df.head(0).assign(trzba=df["cena"].head(0)*df["kusy"].head(0))), ((jine,),jine.assign(trzba=jine["cena"]*jine["kusy"]))]
check_cases(c, ns, 'pridej_trzbu', cases)
c.done()
