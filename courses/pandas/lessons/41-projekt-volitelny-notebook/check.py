import sys,os
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
os.environ.setdefault("MPLBACKEND","Agg")
os.environ.setdefault("MPLCONFIGDIR",str(Path(".matplotlib").resolve()))
from dilna_check import check
from dilna_check.pandas_final import check_stage
c=check()
ns=c.load()
check_stage(c,ns,5)
c.done()
