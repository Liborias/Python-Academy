import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
from pathlib import Path
paths=[]
for i,text in enumerate(['Zlín;-2,5\nBrno;0,0\n', '"Hala; sever";11,75\n', 'Praha;18,0\nOlomouc;12,5\nZlín;-1,0\n']):
    path=c.student.parent/f'jina-bez-hlavicky-{i}.csv';path.write_text(text,encoding='utf-8');paths.append(str(path))

cases=[((path,),pd.read_csv(path,sep=";",decimal=",",encoding="utf-8",header=None,names=["misto","hodnota"])) for path in paths]
check_cases(c,ns,'nacti_bez_hlavicky',cases,readonly_files=[args[0] for args, expected in cases])
c.done()
