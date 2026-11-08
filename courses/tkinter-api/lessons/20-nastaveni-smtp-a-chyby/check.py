import sys
from unittest.mock import patch
import tkinter
from dilna_check import check

c=check();sys.path.insert(0,str(c.student.parent))
with patch.object(tkinter,'Tk',side_effect=RuntimeError('Import nesmí otevřít okno.')):ns=c.load()
if ns and callable(ns.get('nacti_nastaveni')):
    c.returns(ns,'nacti_nastaveni',({},2525),{'host':'127.0.0.1','port':2525,'timeout':2.0})
    data={'DILNA_SMTP_HOST':' 127.0.0.1 ','DILNA_SMTP_PORT':' 23456 ','DILNA_SMTP_TIMEOUT':' 0.25 ','JINA_PROMENNA':'neměnit'}
    before=dict(data)
    c.returns(ns,'nacti_nastaveni',(data,2525),{'host':'127.0.0.1','port':23456,'timeout':.25})
    c.add('Vstupní prostředí se nemění',data==before,'Čtěte předané mapování bez jeho změny.')
    invalid=[{'DILNA_SMTP_HOST':'smtp.example.test'},{'DILNA_SMTP_PORT':'0'},{'DILNA_SMTP_PORT':'65536'},
             {'DILNA_SMTP_PORT':'abc'},{'DILNA_SMTP_TIMEOUT':'0'},{'DILNA_SMTP_TIMEOUT':'-1'},
             {'DILNA_SMTP_TIMEOUT':'nan'},{'DILNA_SMTP_TIMEOUT':'inf'},{'DILNA_SMTP_TIMEOUT':'6'},
             {'DILNA_SMTP_TIMEOUT':'text'},{'DILNA_SMTP_PORT':None}]
    for i,data in enumerate(invalid):
        ok,value=c.call(ns,'nacti_nastaveni',(data,2525))
        c.add('Neplatné nastavení '+str(i),not ok and isinstance(value,ValueError),'Ověřte místní host, rozsah portu a konečný kladný timeout do 5 sekund.')
else:c.add('Funkce nacti_nastaveni',False,'Definujte nacti_nastaveni(prostredi, vychozi_port).')

send='Předat místnímu záchytu'
wait={'action':'wait','until':{'text':send,'state':'normal'},'timeout':2}
actions=[{'action':'click','text':'Opožděné potvrzení'},{'action':'click','text':send},{'action':'click','text':send},
         {'action':'click','text':'Odmítnutí příjemce'},{'action':'wait','ms':120},{'action':'click','text':'Zkontrolovat záchyt'},wait,
         {'action':'click','text':'Odmítnutí příjemce'},{'action':'click','text':send},wait,
         {'action':'click','text':'Přijetí'},{'action':'click','text':send},wait]
base_env={'DILNA_SMTP_HOST':'127.0.0.1','DILNA_SMTP_TIMEOUT':'2'}
r=c.tk_run(actions,extra_env=base_env)
if c.tk_no_error(r):
    status=[w for w in r.widgets('label') if w['text']=='Zpráva zatím nebyla předána.']
    counts=[w for w in r.widgets('label') if w['text']=='Zachyceno: 0']
    preview=r.widgets('text')
    pending='Předávám zprávu místnímu záchytu...';received='Zprávu převzal místní záchyt.';refused='Příjemce byl odmítnut. Zpráva nebyla převzata.'
    expected=[('Zpráva zatím nebyla předána.',0,False),('Zpráva zatím nebyla předána.',0,False),
              (pending,0,True),(pending,0,True),(pending,0,True),(pending,0,True),(pending,1,True),
              (received,1,False),(received,1,False),(pending,1,True),(refused,1,False),(refused,1,False),(pending,1,True),(received,2,False)]
    for i,(message,count,busy) in enumerate(expected):
        widgets=r.widgets(index=i);by_id={w['id']:w for w in widgets};texts=r.widgets('text',i)
        buttons=[w for w in r.widgets('button',i) if w['text']==send];radios=r.widgets('radiobutton',i)
        ok=len(status)==len(counts)==len(texts)==len(buttons)==1 and len(radios)==3
        ok=ok and by_id.get(status[0]['id'],{}).get('text')==message and by_id.get(counts[0]['id'],{}).get('text')==f'Zachyceno: {count}'
        ok=ok and texts[0]['state']=='disabled' and (buttons[0]['state']=='disabled')==busy and all((w['state']=='disabled')==busy for w in radios)
        ok=ok and (('Předmět: Zkouška nastavení' in texts[0]['value']) if count else texts[0]['value']=='Místní záchyt je prázdný.')
        ok=ok and len(widgets)==len(r.widgets()) and all(w['visible'] for w in widgets)
        c.add('SMTP, náhled a stav '+str(i),ok,'Běží právě jedno předání, náhled jde kontrolovat při čekání. Přijetí a odmítnutí se rozlišují, nový pokus je ruční.')
    c.add('Hlavní smyčka nečeká na SMTP',all(row['ms']<250 for row in r.callbacks or []),'Přenos běží v pracovníkovi a Tk se mění jen v hlavním vlákně.')

short=c.tk_run([{'action':'click','text':'Opožděné potvrzení'},{'action':'click','text':send},wait,{'action':'wait','ms':450},{'action':'click','text':'Zkontrolovat záchyt'}],
               extra_env={'DILNA_SMTP_HOST':'127.0.0.1','DILNA_SMTP_TIMEOUT':'0.05'})
if c.tk_no_error(short,'Krátký timeout se vrátí do okna'):
    labels=[w['text'] for w in short.widgets('label',-1)]
    c.add('Nejisté potvrzení bez automatické duplicity','Přenos není potvrzený. Před novým pokusem zkontrolujte záchyt.' in labels and 'Zachyceno: 1' in labels,
          'Timeout neprokazuje, že server nic nepřevzal. Neopakujte předání automaticky.')
for env in [{'DILNA_SMTP_PORT':'0'},{'DILNA_SMTP_HOST':'smtp.example.test'}]:
    invalid=c.tk_run([{'action':'click','text':send}],extra_env=env)
    if c.tk_no_error(invalid,'Neplatné prostředí neotevře SMTP'):
        labels=[w['text'] for w in invalid.widgets('label',-1)]
        c.add('Chybné nastavení se zobrazí','Neplatné nastavení. Opravte proměnné prostředí a spusťte program znovu.' in labels and 'Zachyceno: 0' in labels,
              'Odmítněte nesprávné nastavení před spuštěním pracovníka.')
c.done()
