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
for values,edges,density in [([0,1,2,4],[0,1,4],[0.25,0.25]),([0,0,1,3],[0,1,3],[0.5,0.25]),([-2,0,0.5,2,8],[0,1,5],[2/3,1/12])]:
    cases.append(((values,edges),{"axes":[{'title': 'Hustota dob', 'xlabel': 'Doba (min)', 'ylabel': 'Hustota (1/min)',"bars":density,"edges":edges}]}))

check_figures(c, ns, 'hustota', cases)
c.done()
