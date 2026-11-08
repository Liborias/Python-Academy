import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()

cases=[(({"caj":45,"kava":60},"cena"),pd.Series({"caj":45,"kava":60},name="cena",dtype="float64")), (({},"nic"),pd.Series({},name="nic",dtype="float64")), (({"B":-2,"A":None},"test"),pd.Series({"B":-2,"A":None},name="test",dtype="float64"))]
check_cases(c,ns,'serie_ze_slovniku',cases)
c.done()
