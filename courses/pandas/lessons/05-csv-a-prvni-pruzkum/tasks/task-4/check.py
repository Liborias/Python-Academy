import pandas as pd
from dilna_check import check
from dilna_check.pandas_tools import check_cases

c=check();ns=c.load()
from pathlib import Path
paths=[]
for i,text in enumerate(['kod;nazev;kusy\n000;Čaj;0\n007;Voda;2\n', 'kod;nazev;kusy\n0012;"Čaj; zelený";9\n', 'kod;nazev;kusy\n']):
    path=c.student.parent/f'jine-kody-{i}.csv';path.write_text(text,encoding='utf-8');paths.append(str(path))

cases=[((path,),pd.read_csv(path,sep=";",encoding="utf-8",dtype={"kod":"str"})) for path in paths]
check_cases(c,ns,'nacti_identifikatory',cases,readonly_files=[args[0] for args, expected in cases])
c.done()
