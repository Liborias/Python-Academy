import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dilna_check import check
from dilna_check.pandas_files import excel_cases
c=check()
ns=c.load()
excel_cases(c,ns,1)
c.done()
