import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from dilna_check import check
from dilna_check.bmi_tracker import over
c = check()
over(c, 3)
c.done()
