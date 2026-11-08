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
for x,y,sizes in [([3,1],[8,4],[25,100]),([],[],[]),([2,2,5],[0,-1,9],[10,40,90])]:
    cases.append(((x,y,sizes),{"axes":[{'title': 'Velikost značky jako údaj', 'xlabel': 'Čas (min)', 'ylabel': 'Výkon (body)',"points":[{"x":x,"y":y,"sizes":sizes}]}]}))

check_figures(c, ns, 'velikost_bodu', cases)
c.done()
