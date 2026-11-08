from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()

for labels in [("Cesta","Čas (s)","Dráha (m)"),("","Den","Teplota (°C)")]:
    fig=Figure();ax=fig.subplots();line,=ax.plot([2,5],[7,9]);ax.set_xlim(1,8);ax.set_ylim(-2,12)
    ok,result=c.call(ns,"popis_osu",(ax,*labels))
    c.add("Původní osa, čára a rozsah",ok and result is ax and ax.figure is fig and len(fig.axes)==1 and list(ax.lines)==[line] and near(line.get_xdata(),[2,5]) and near(line.get_ydata(),[7,9]) and near(ax.get_xlim(),[1,8]) and near(ax.get_ylim(),[-2,12]),"Popisky doplňte do předané osy bez mazání dat nebo změny rozsahu.")
    c.add("Titulek a oba popisky",(ax.get_title(),ax.get_xlabel(),ax.get_ylabel())==labels,"Použijte všechny tři předané texty.")
c.done()
