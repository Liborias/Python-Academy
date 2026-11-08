import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
from pathlib import Path
paths=[]
for i,text in enumerate(['produkt,cena\n"Čaj, velký",45.5\nKáva,0.0\n', 'produkt,cena\nVoda,12.75\n', 'produkt,cena\n']):
    path=c.student.parent/f'jiny-cenik-{i}.csv';path.write_text(text,encoding='utf-8');paths.append(str(path))

cases=[((path,),pd.read_csv(path,encoding="utf-8")) for path in paths]
check_cases(c,ns,'nacti_cenik',cases,readonly_files=[args[0] for args, expected in cases])
c.done()
