import sys
from pathlib import Path
from dilna_check import check
c=check();ns=c.load();work=c.student.parent
source=work/'český projekt s mezerou';source.mkdir()
script=source/'aplikace.py';script.write_text('print("Dílna")\n',encoding='utf-8')
out=work/'výstup s mezerou';python='C:/Python s mezerou/python.exe'

def option(cmd,name):
    try:return cmd[cmd.index(name)+1] if cmd.count(name)==1 else None
    except (ValueError,IndexError):return None

for include in (False,True):
    if include:(source/'data').mkdir()
    before={str(p.relative_to(work)) for p in work.rglob('*')}
    ok,cmd=c.call(ns,'prikaz_sestaveni',(python,str(script),str(out),'MojeDilna'))
    good=ok and isinstance(cmd,list) and all(isinstance(v,str) for v in cmd)
    if good:
        good=cmd[:3]==[python,'-m','PyInstaller'] and cmd[-1]==str(script.resolve())
        good=good and all(cmd.count(k)==1 for k in ('--noconfirm','--clean','--onedir','--console')) and '--onefile' not in cmd and '--windowed' not in cmd
        good=good and option(cmd,'--name')=='MojeDilna' and all(option(cmd,'--'+flag)==str(out.resolve()/suffix) for flag,suffix in [('distpath','dist'),('workpath','build'),('specpath','spec')])
        good=good and (option(cmd,'--add-data')==str(source/'data')+':data' if include else '--add-data' not in cmd)
    c.add('Přesné argumenty a cesty '+str(include),good,'Vraťte seznam pro stejný interpreter, onedir/console, oddělené výstupy a případnou složku data. Cesty s mezerami zůstávají jediným argumentem.')
    c.add('Plán nic nevytváří',before=={str(p.relative_to(work)) for p in work.rglob('*')},'Funkce jen sestaví seznam; stavbu spouští až samostatný sestavit.py.')
for args in [('',script,out), (None,script,out), (python,source,out), (python,source/'chybi.py',out), (python,script,out,'../ven'),
             (python,script,out,'Název'),(python,script,out,'1Dilna'),(python,script,out,''),(python,script,out,True)]:
    c.raises(ns,'prikaz_sestaveni',args,ValueError,'Ověřte interpreter, existující .py a bezpečný neprázdný název ASCII začínající písmenem.')
wrong=source/'text.txt';wrong.write_text('a',encoding='utf-8');c.raises(ns,'prikaz_sestaveni',(python,wrong,out),ValueError)
ok,cmd=c.call(ns,'prikaz_sestaveni',(python,script,out))
c.add('Výchozí název',ok and isinstance(cmd,list) and option(cmd,'--name')=='KorespondencniDilna','Zachovejte výchozí název nebo použijte předaný název.')
r=c.run()
if c.no_error(r):c.add('Ukázka vysvětlí připravený příkaz','PyInstaller' in r.out and 'Argumenty' in r.out,'V hlavním bloku příkaz jen vypište, skutečné sestavení je volitelné.')
c.done()
