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
for names,values in [(["Dlouhý název","Krátký"],[3,0]),([],[]),(["A","B","C"],[1.5,4.0,2.0])]:
    cases.append(((names,values),{"axes":[{'title': 'Kategorie shora', 'xlabel': 'Počet', 'ylabel': 'Kategorie',"bars":values,"ticks":names,"horizontal":True,"inverted_y":True,"zero":"x"}]}))

check_figures(c, ns, 'vodorovne', cases)
c.done()
