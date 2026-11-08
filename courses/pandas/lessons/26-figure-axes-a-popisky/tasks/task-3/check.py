from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()

for labels in [("Ráno","Večer"),("Plán","Skutečnost")]:
    fig=Figure();ax=fig.subplots();ax.plot([1,2],[3,4],label=labels[0]);ax.plot([1,2],[6,5],label=labels[1]);lines=list(ax.lines)
    ok,result=c.call(ns,"pridej_legendu",(ax,));legend=ax.get_legend()
    c.add("Legenda původních čar",ok and result is ax and list(ax.lines)==lines and all(near(line.get_xdata(),[1,2]) and near(line.get_ydata(),[3,4] if i==0 else [6,5]) for i,line in enumerate(lines)) and legend is not None and [t.get_text() for t in legend.get_texts()]==list(labels),"Přidejte legendu podle label čar a vraťte původní osu.")
c.done()
