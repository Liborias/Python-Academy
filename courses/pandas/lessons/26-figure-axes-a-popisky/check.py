from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()

check_figures(c, ns, 'priprav_graf', [(("Měření", "Den", "Teplota (°C)"), {"size":[6,4],"axes":[{"title":"Měření","xlabel":"Den","ylabel":"Teplota (°C)"}]}), (("", "Čas (s)", "Dráha (m)"), {"size":[6,4],"axes":[{"title":"","xlabel":"Čas (s)","ylabel":"Dráha (m)"}]})])
c.done()
