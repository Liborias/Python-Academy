from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()
s=pd.Series([None,0.0,2.0,None,4.0],index=["a","b","c","d","e"],name="doba",dtype="float64")

check_cases(c, ns, 'vycisti_hodnoty', [((s,),s.iloc[[1,2,4]]), ((s.iloc[:0],),s.iloc[:0]), ((s.iloc[[0,3]],),s.iloc[:0]), ((s.rename("X"),),s.iloc[[1,2,4]].rename("X"))])
c.done()
