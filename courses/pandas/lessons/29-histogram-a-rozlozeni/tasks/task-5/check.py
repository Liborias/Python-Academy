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
for a,b,edges,ca,cb in [([0,1,2],[1,1,3,4],[0,2,4],[2,1],[2,2]),([],[1,1,1],[0,1,3],[0,0],[0,3]),([],[],[0,2,5],[0,0],[0,0])]:
    cases.append(((a,b,edges),{"title":"Dvě rozložení","row":True,"shared_y":True,"axes":[{'title': 'Ráno', 'xlabel': 'Doba (min)', 'ylabel': 'Četnost',"bars":ca,"edges":edges},{'title': 'Večer', 'xlabel': 'Doba (min)', 'ylabel': 'Četnost',"bars":cb,"edges":edges}]}))

check_figures(c, ns, 'dve_rozlozeni', cases)
c.done()
