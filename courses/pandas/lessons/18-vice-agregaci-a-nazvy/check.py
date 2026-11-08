import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"skupina":["B","A","B",None,"C","A","C"],"hodnota":[10.0,0.0,None,5.0,None,20.0,None],"jina":[1.0,2.0,3.0,4.0,5.0,None,7.0],"pobocka":["Y","X","X","Y","X","X",None]},index=["r6","r1","r5","r2","r0","r4","r3"])
expected=pd.DataFrame({"count":[2,1,0,1],"mean":[10.0,10.0,None,5.0],"min":[0.0,10.0,None,5.0],"max":[20.0,10.0,None,5.0]},index=pd.Index(["A","B","C",None],dtype="str",name="skupina"))

cases = [((df,"skupina","hodnota"),expected), ((df.head(0),"skupina","hodnota"),df.head(0).groupby("skupina",dropna=False)["hodnota"].agg(["count","mean","min","max"])), ((df,"pobocka","jina"),df.groupby("pobocka",dropna=False,sort=True)["jina"].agg(["count","mean","min","max"]))]
check_cases(c, ns, 'statistiky_skupin', cases)
c.done()
