import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dilna_check import check
from dilna_check.pandas_files import pipeline_cases
c=check()
ns=c.load()
pipeline_cases(c,ns,4)
c.done()
