import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()

cases=[(([18,21.5,16],["Brno","Praha","Zlin"],"teplota"),pd.Series([18,21.5,16],index=["Brno","Praha","Zlin"],name="teplota",dtype="float64")), (([],[],"prazdne"),pd.Series([],index=[],name="prazdne",dtype="float64")), (([0,-4.5,None],["C","A","B"],"hodnota"),pd.Series([0,-4.5,None],index=["C","A","B"],name="hodnota",dtype="float64"))]
check_cases(c,ns,'vytvor_mereni',cases)
c.done()
