from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()

check_cases(c, ns, 'cetnosti', [(([0,1,2,2,3,4,6],[0,2,4,6]),[2,3,2]), (([],[0,1,4]),[0,0]), (([-1,0,1,4,5],[0,1,4]),[1,2]), (([1,1,1],[0,1,2]),[0,3])])
c.done()
