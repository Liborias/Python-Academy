from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()
a=pd.DataFrame({"x":[3.0,1.0],"y":[4.0,2.0]});b=pd.DataFrame({"x":[0.0],"y":[-2.0]})
cases=[]
for first,second in [(a,b),(a.head(0),b),(a.head(0),b.head(0))]:
    cases.append(((first,second),{"axes":[{'title': 'Dvě skupiny', 'xlabel': 'x', 'ylabel': 'y',"points":[{"x":first["x"],"y":first["y"]},{"x":second["x"],"y":second["y"]}],"legend":["Skupina A","Skupina B"]}]}))

check_figures(c, ns, 'porovnej_skupiny', cases)
c.done()
