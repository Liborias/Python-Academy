import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"skupina":["B","A","B",None,"C","A","C"],"hodnota":[10.0,0.0,None,5.0,None,20.0,None],"jina":[1.0,2.0,3.0,4.0,5.0,None,7.0],"pobocka":["Y","X","X","Y","X","X",None]},index=["r6","r1","r5","r2","r0","r4","r3"])
expected=pd.Series([2,1,0,1],index=pd.Index(["A","B","C",None],dtype="str",name="skupina"),name="hodnota",dtype="int64")

cases = [((df,"skupina","hodnota"),expected), ((df,"skupina","jina"),df.groupby("skupina",dropna=False,sort=True)["jina"].count()), ((df.head(0),"skupina","hodnota"),df.head(0).groupby("skupina",dropna=False)["hodnota"].count())]
check_cases(c, ns, 'dostupne_ve_skupinach', cases)
c.done()
