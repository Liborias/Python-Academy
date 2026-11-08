from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()

for lo,hi in [(-10,30),(2,8),(0,100)]:
    fig=Figure();ax=fig.subplots();line,=ax.plot([2,5],[3,4]);ax.set_xlim(1,7)
    ok,result=c.call(ns,"nastav_rozsah",(ax,lo,hi))
    c.add("Zadané meze y bez změny dat a x",ok and result is ax and near(ax.get_ylim(),[lo,hi]) and near(ax.get_xlim(),[1,7]) and list(ax.lines)==[line] and near(line.get_xdata(),[2,5]) and near(line.get_ydata(),[3,4]),"Nastavte pouze ylim na předané minimum a maximum.")
c.done()
