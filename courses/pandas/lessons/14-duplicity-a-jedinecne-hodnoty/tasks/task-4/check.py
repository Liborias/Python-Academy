import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["B","A","B","","C","A"],name="misto",dtype="str")
extra=pd.Series(["Žďár","Brno","Žďár"],dtype="str")

cases = [((s,),["B","A","","C"]), ((s.iloc[:0],),[]), ((extra,),["Žďár","Brno"])]
check_cases(c, ns, 'jedinecne_hodnoty', cases)
c.done()
