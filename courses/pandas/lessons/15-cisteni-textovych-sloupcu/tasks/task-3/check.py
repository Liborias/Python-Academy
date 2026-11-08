import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series([" 12 kg ","kg12","12 kg navic",None,"kg"],index=["E","B","A","D","C"],name="hmotnost",dtype="str")
extra=pd.Series(["abc.cz","a.cz.txt","cz"],name="web",dtype="str")

cases = [((s,"kg"),pd.Series(["12","kg12","12 kg navic",None,""],index=s.index,name=s.name,dtype="str")), ((s.iloc[:0],"kg"),s.iloc[:0]), ((extra,".cz"),pd.Series(["abc","a.cz.txt","cz"],name="web",dtype="str"))]
check_cases(c, ns, 'odstran_jednotku', cases)
c.done()
