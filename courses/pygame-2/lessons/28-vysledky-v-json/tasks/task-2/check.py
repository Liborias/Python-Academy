import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from dilna_check import check
from dilna_check.predani_hry import over
c = check()
ns = c.load()
over(c, ns, 2, 1)
c.done()
