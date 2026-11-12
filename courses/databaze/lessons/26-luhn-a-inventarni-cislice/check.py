import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dilna_check import check
from dilna_check.predani_pujcovny import over
c=check()
over(c,0)
c.done()
