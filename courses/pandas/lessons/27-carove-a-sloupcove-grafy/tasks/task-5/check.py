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
for x,y in [([5.,1.,3.,3.],[8.,2.,7.,6.]),([],[]),([3.,1.],[float("nan"),0.]),([3.,1.,3.,2.]*10,[float(i) for i in range(40)])]:
    df=pd.DataFrame({"den":x,"hodnota":y},dtype="float64");order=sorted(range(len(x)),key=lambda i:x[i])
    cases.append(((df,),{"axes":[{'title': 'Seřazený vývoj', 'xlabel': 'Den', 'ylabel': 'Hodnota',"lines":[{"x":[x[i] for i in order],"y":[y[i] for i in order],"marker":"o"}]}]}))

check_figures(c, ns, 'serazeny_vyvoj', cases)
c.done()
