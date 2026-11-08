from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()
cases=[]
for x,y in [([1,3,7],[2.0,None,4.0]),([],[]),([2,5],[0.0,-3.0])]:
    y=[float("nan") if v is None else v for v in y]
    cases.append(((x,y),{"axes":[{'title': 'Vývoj měření', 'xlabel': 'Den', 'ylabel': 'Hodnota',"lines":[{"x":x,"y":y,"marker":"o"}]}]}))

check_figures(c, ns, 'vyvoj', cases)
c.done()
