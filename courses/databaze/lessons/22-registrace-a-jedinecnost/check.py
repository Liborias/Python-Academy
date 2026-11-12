import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from dilna_check import check
from dilna_check.mistni_ucty import over
c = check()
over(c, 1)
c.done()
