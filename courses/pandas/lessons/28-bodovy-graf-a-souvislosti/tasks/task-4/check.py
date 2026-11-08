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
for x,y,lo,hi in [([1,3],[2,4],0,6),([],[],-2,2),([-3,0],[0,3],-5,5)]:
    cases.append(((x,y,lo,hi),{"axes":[{'title': 'Stejné měřítko', 'xlabel': 'Východ (m)', 'ylabel': 'Sever (m)',"points":[{"x":x,"y":y}],"xlim":[lo,hi],"ylim":[lo,hi],"equal":True}]}))

check_figures(c, ns, 'stejne_meritko', cases)
c.done()
