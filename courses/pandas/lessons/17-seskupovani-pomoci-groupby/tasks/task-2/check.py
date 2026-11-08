import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"skupina":["B","A","B",None,"C","A","C"],"hodnota":[10.0,0.0,None,5.0,None,20.0,None],"jina":[1.0,2.0,3.0,4.0,5.0,None,7.0],"pobocka":["Y","X","X","Y","X","X",None]},index=["r6","r1","r5","r2","r0","r4","r3"])
expected=pd.Series([2,2,2,1],index=pd.Index(["A","B","C",None],dtype="str",name="skupina"),dtype="int64")

cases = [((df,"skupina"),expected), ((df.head(0),"skupina"),df.head(0).groupby("skupina",dropna=False).size()), ((df,"pobocka"),df.groupby("pobocka",dropna=False,sort=True).size())]
check_cases(c, ns, 'pocet_radku_skupin', cases)
c.done()
