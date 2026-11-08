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
for x,y in [([3,1,2],[8,7,4]),([],[]),([1,1,4],[0,-2,9])]:
    cases.append(((x,y),{"axes":[{'title': 'Cvičná měření', 'xlabel': 'Doba učení (h)', 'ylabel': 'Body v kvízu',"points":[{"x":x,"y":y}]}]}))

check_figures(c, ns, 'bodovy_graf', cases)
c.done()
