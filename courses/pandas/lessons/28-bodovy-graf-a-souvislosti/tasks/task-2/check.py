from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()
df=pd.DataFrame({"x":[1.0,None,0.0,4.0],"y":[None,2.0,0.0,3.0],"jine":[8.0,9.0,None,None]},index=["a","b","c","d"])

check_cases(c, ns, 'vyber_dvojice', [((df,),pd.DataFrame({"x":[0.0,4.0],"y":[0.0,3.0]},index=["c","d"])),((df.head(0),),df.head(0)[["x","y"]]),((df.iloc[:2],),df.iloc[:0][["x","y"]])])
c.done()
