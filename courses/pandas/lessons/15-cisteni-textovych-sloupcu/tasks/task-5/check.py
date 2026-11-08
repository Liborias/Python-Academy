import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c = check()
ns = c.load()
df=pd.DataFrame({"misto":[" PRAHA ","Praha",None,""],"poznamka":[" Zachovat ","Text"," X ",None],"kusy":[1,2,3,0]},index=["D","A","C","B"])
a=df.copy();a["misto"]=["praha","praha",None,""]
b=df.copy();b["poznamka"]=["zachovat","text","x",None]

cases = [((df,"misto"),a), ((df,"poznamka"),b), ((df.head(0),"misto"),df.head(0))]
check_cases(c, ns, 'vycisti_sloupec', cases)
c.done()
