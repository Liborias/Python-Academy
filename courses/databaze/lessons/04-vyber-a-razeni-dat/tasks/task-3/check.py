import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from dilna_check import check
from dilna_check.sqlite_intro import over
c = check()
ns = c.load()
over(c, ns, 3, 2)
c.done()
