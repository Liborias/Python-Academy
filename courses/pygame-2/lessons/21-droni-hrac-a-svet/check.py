import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dilna_check import check
from dilna_check.droni import over
c=check()
ns=c.load()
over(c,ns,0)
c.done()
