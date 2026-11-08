import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"skupina":["B","A","B",None,"C","A","C"],"hodnota":[10.0,0.0,None,5.0,None,20.0,None],"jina":[1.0,2.0,3.0,4.0,5.0,None,7.0],"pobocka":["Y","X","X","Y","X","X",None]},index=["r6","r1","r5","r2","r0","r4","r3"])
expected=pd.DataFrame({"skupina":["A","B","C",None],"hodnota":[20.0,10.0,None,5.0]})
renamed=df.rename(columns={"skupina":"oddil","hodnota":"body"})

cases = [((df,"skupina","hodnota"),expected), ((df.head(0),"skupina","hodnota"),df.head(0).groupby("skupina",as_index=False,dropna=False)["hodnota"].sum(min_count=1)), ((renamed,"oddil","body"),expected.rename(columns={"skupina":"oddil","hodnota":"body"}))]
check_cases(c, ns, 'seskup_do_tabulky', cases)
c.done()
