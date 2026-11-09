import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from dilna_check import check
from dilna_check.meteority import over
c = check()
ns = c.load()
over(c, ns, 3)
c.done()
