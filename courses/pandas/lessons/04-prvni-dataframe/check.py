import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
data={"misto":["Brno","Praha","Zlin"],"hodnota":[2.5,None,-1],"aktivni":[True,False,True]}

cases=[((data,),pd.DataFrame(data)), (({},),pd.DataFrame({})), (({"kod":[],"hodnota":[]},),pd.DataFrame({"kod":[],"hodnota":[]}))]
check_cases(c,ns,'vytvor_tabulku',cases)
c.done()
