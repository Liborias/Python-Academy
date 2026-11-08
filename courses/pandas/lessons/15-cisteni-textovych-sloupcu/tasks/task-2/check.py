import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
s=pd.Series(["  Nové   Město ","Žďár\tnad\nSázavou",None,"\t ","A\u00a0B"],index=["E","B","A","D","C"],name="misto",dtype="str")

cases = [((s,),pd.Series(["Nové Město","Žďár nad Sázavou",None,"","A B"],index=s.index,name=s.name,dtype="str")), ((s.iloc[:0],),s.iloc[:0])]
check_cases(c, ns, 'sjednot_mezery', cases)
c.done()
