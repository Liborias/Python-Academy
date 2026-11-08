import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"skupina":["B","A","B",None,"C","A","C"],"hodnota":[10.0,0.0,None,5.0,None,20.0,None],"jina":[1.0,2.0,3.0,4.0,5.0,None,7.0],"pobocka":["Y","X","X","Y","X","X",None]},index=["r6","r1","r5","r2","r0","r4","r3"])

cases = [((df,"skupina","pobocka","hodnota"),df.groupby(["skupina","pobocka"],as_index=False,dropna=False,sort=True).agg(radky=("hodnota","size"),prumer=("hodnota","mean"))), ((df,"pobocka","skupina","jina"),df.groupby(["pobocka","skupina"],as_index=False,dropna=False,sort=True).agg(radky=("jina","size"),prumer=("jina","mean"))), ((df.head(0),"skupina","pobocka","hodnota"),df.head(0).groupby(["skupina","pobocka"],as_index=False,dropna=False).agg(radky=("hodnota","size"),prumer=("hodnota","mean")))]
check_cases(c, ns, 'prehled_dvou_klicu', cases)
c.done()
