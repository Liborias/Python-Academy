from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()

check_figures(c, ns, 'dva_panely', [(("Dva pohledy",),{"size":[8,3],"row":True,"title":"Dva pohledy","axes":[{},{}]}), (("Český přehled",),{"size":[8,3],"row":True,"title":"Český přehled","axes":[{},{}]})])
c.done()
