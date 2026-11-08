import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
data={"misto":["Brno","Praha"],"hodnota":[2.5,None]}

cases=[((data,["B","A"]),pd.DataFrame(data,index=["B","A"])), (({"hodnota":[]},[]),pd.DataFrame({"hodnota":[]},index=[]))]
check_cases(c,ns,'pojmenuj_radky',cases)
c.done()
