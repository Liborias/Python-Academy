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
for x,a,b in [([1,4],[8.0,10.0],[6.0,7.0]),([],[],[]),([2,5,6],[-1.0,float("nan"),3.0],[0.0,2.0,4.0])]:
    cases.append(((x,a,b),{"axes":[{'title': 'Dvě měření', 'xlabel': 'Den', 'ylabel': 'Teplota (°C)',"lines":[{"x":x,"y":a,"marker":"o"},{"x":x,"y":b,"marker":"s"}],"legend":["Ráno","Večer"]}]}))

check_figures(c, ns, 'dve_rady', cases)
c.done()
