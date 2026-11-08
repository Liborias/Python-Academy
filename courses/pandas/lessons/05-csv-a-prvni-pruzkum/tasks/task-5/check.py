import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
from pathlib import Path
work=c.student.parent
paths=[]
for i,text in enumerate(['misto;teplota;vlhkost\nBrno;18,5;65\nPraha;-2,0;58\n', 'misto;teplota;vlhkost\n"Řádek\ns pokračováním";0,0;10\n', 'misto;teplota;vlhkost\n']):
    p=work/f'vlastni-{i}.csv';p.write_text(text,encoding='utf-8');paths.append(str(p))

cases=[((p,),len(pd.read_csv(p,sep=";",decimal=",",encoding="utf-8"))) for p in paths]
check_cases(c,ns,'pocet_zaznamu',cases,readonly_files=[args[0] for args, expected in cases])
c.done()
