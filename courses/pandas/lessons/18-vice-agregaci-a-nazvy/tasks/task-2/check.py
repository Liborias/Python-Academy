import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"skupina":["B","A","B",None,"C","A","C"],"hodnota":[10.0,0.0,None,5.0,None,20.0,None],"jina":[1.0,2.0,3.0,4.0,5.0,None,7.0],"pobocka":["Y","X","X","Y","X","X",None]},index=["r6","r1","r5","r2","r0","r4","r3"])
expected=pd.DataFrame({"skupina":["A","B","C",None],"radky":[2,2,2,1],"dostupne":[2,1,0,1],"prumer":[10.0,10.0,None,5.0]})

cases = [((df,"skupina","hodnota"),expected), ((df.head(0),"skupina","hodnota"),df.head(0).groupby("skupina",as_index=False,dropna=False).agg(radky=("hodnota","size"),dostupne=("hodnota","count"),prumer=("hodnota","mean"))), ((df,"pobocka","jina"),df.groupby("pobocka",as_index=False,dropna=False,sort=True).agg(radky=("jina","size"),dostupne=("jina","count"),prumer=("jina","mean")))]
check_cases(c, ns, 'pojmenovany_prehled', cases)
c.done()
