import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"skupina":["B","A","B",None,"C","A","C"],"hodnota":[10.0,0.0,None,5.0,None,20.0,None],"jina":[1.0,2.0,3.0,4.0,5.0,None,7.0],"pobocka":["Y","X","X","Y","X","X",None]},index=["r6","r1","r5","r2","r0","r4","r3"])
extra=pd.DataFrame({"typ":["A","A","A","B"],"cislo":[10.0,10.0,1000.0,20.0]})
expected=pd.DataFrame({"typ":["A","B"],"dostupne":[3,1],"prumer":[340.0,20.0],"median":[10.0,20.0]})

cases = [((df,"skupina","hodnota"),df.groupby("skupina",as_index=False,dropna=False,sort=True).agg(dostupne=("hodnota","count"),prumer=("hodnota","mean"),median=("hodnota","median"))), ((df.head(0),"skupina","hodnota"),df.head(0).groupby("skupina",as_index=False,dropna=False).agg(dostupne=("hodnota","count"),prumer=("hodnota","mean"),median=("hodnota","median"))), ((extra,"typ","cislo"),expected)]
check_cases(c, ns, 'porovnej_skupiny', cases)
c.done()
