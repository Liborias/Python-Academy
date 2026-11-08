import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
rows=[{"misto":"Brno","hodnota":2.5,"navic":7},{"misto":"Praha"}]

cases=[((rows,["hodnota","misto"]),pd.DataFrame(rows,columns=["hodnota","misto"])), (([],["misto","hodnota"]),pd.DataFrame([],columns=["misto","hodnota"])), ((rows,["misto"]),pd.DataFrame(rows,columns=["misto"]))]
check_cases(c,ns,'tabulka_ze_zaznamu',cases)
c.done()
