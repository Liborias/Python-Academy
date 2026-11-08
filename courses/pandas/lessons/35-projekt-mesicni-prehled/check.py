import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dilna_check import check
from dilna_check.pandas_files import project_cases
c=check()
ns=c.load()
project_cases(c,ns)
c.done()
