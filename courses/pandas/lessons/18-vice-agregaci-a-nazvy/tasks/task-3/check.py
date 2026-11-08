import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"skupina":["B","A","B",None,"C","A","C"],"hodnota":[10.0,0.0,None,5.0,None,20.0,None],"jina":[1.0,2.0,3.0,4.0,5.0,None,7.0],"pobocka":["Y","X","X","Y","X","X",None]},index=["r6","r1","r5","r2","r0","r4","r3"])
expected=pd.DataFrame({"skupina":["A","B","C",None],"prumer":[10.0,10.0,None,5.0],"maximum":[2.0,3.0,7.0,4.0]})

cases = [((df,"skupina","hodnota","jina"),expected), ((df,"skupina","jina","hodnota"),df.groupby("skupina",as_index=False,dropna=False,sort=True).agg(prumer=("jina","mean"),maximum=("hodnota","max"))), ((df.head(0),"skupina","hodnota","jina"),df.head(0).groupby("skupina",as_index=False,dropna=False).agg(prumer=("hodnota","mean"),maximum=("jina","max")))]
check_cases(c, ns, 'prehled_dvou_hodnot', cases)
c.done()
