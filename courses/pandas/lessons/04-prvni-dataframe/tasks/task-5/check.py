import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()

cases=[((pd.DataFrame({"A":[1,2,3],"B":[4,5,6]}),),(3,2)), ((pd.DataFrame(columns=["A","B"]),),(0,2)), ((pd.DataFrame(),),(0,0))]
check_cases(c,ns,'rozmery_tabulky',cases)
c.done()
