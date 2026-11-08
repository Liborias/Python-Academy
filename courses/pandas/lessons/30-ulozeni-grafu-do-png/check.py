from dilna_check import check
from dilna_check.matplotlib_tools import check_figures, figure_matches, near
from dilna_check.pandas_tools import check_cases, equivalent
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from pathlib import Path

c = check()
ns = c.load()

from dilna_check.matplotlib_tools import check_exports
check_exports(c,ns,"uloz_png","png")
c.done()
