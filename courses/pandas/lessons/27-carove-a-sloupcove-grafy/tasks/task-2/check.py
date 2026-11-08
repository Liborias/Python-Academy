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
for names,counts in [(["Čaj","Káva","Voda"],[4,0,7]),([],[]),(["B","A"],[2.5,1.0])]:
    cases.append(((names,counts),{"axes":[{'title': 'Porovnání kategorií', 'xlabel': 'Kategorie', 'ylabel': 'Počet',"bars":counts,"ticks":names,"zero":"y"}]}))

check_figures(c, ns, 'porovnani', cases)
c.done()
