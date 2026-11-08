import sys
from unittest.mock import patch
import tkinter
from dilna_check import check

c = check()
sys.path.insert(0, str(c.student.parent))
with patch.object(tkinter, "Tk", side_effect=RuntimeError("Import nesmí otevřít okno.")):
    ns = c.load()
work = c.student.parent


def named(r, name, index=-1):
    return next((w for w in r.widgets(index=index) if w.get("name") == name), {})


def fill(name, value):
    return {"action": "fill_text" if name == "telo" else "fill", "name": name, "value": value}


def click(text):
    return {"action": "click", "text": text}

import queue
import smtplib
from zpravy import vytvor_zpravu
if ns:
    message=vytvor_zpravu('eva@example.test','jan@example.test','Snímek','Český text')
    for error,expected in [(None,'prijato'),(smtplib.SMTPRecipientsRefused({'a':(550,b'no')}),'odmitnuto'),
                           (TimeoutError('timeout'),'nejiste'),(smtplib.SMTPServerDisconnected('timeout'),'nejiste'),
                           (OSError('connection'),'chyba'),(smtplib.SMTPDataError(554,b'no'),'chyba')]:
        q=queue.Queue();before=message.as_bytes()
        with patch.dict(ns,odesli_do_zachytu=__import__('unittest.mock',fromlist=['Mock']).Mock(side_effect=error)):
            ok,result=c.call(ns,'predat_zpravu',(message,'127.0.0.1',43210,.2,q))
            mock=ns['odesli_do_zachytu']
            c.add('Předání a výsledek '+expected+str(type(error)),ok and result is None and mock.call_args_list==[__import__('unittest.mock',fromlist=['call']).call(message,'127.0.0.1',43210,.2)]
                  and list(q.queue)==[expected] and message.as_bytes()==before,'Použijte původní zprávu a nastavení; do fronty patří právě jeden stav, očekávané chyby neuniknou z pracovníka.')

send='Předat místnímu záchytu';pending='Předávám zprávu místnímu záchytu...'
wait={'action':'wait','until':{'text':send,'state':'normal'},'timeout':2}
form=[fill('prijemce','jan@example.test'),fill('predmet','Původní snímek'),fill('telo','Původní text\n')]
actions=form+[click('Opožděné potvrzení'),click(send),click(send),fill('predmet','Nový koncept'),fill('telo','Další práce\n'),
              {'action':'wait','ms':120},click('Zkontrolovat záchyt'),wait,
              click('Odmítnutí příjemce'),click(send),wait,click('Přijetí'),click(send),wait]
r=c.tk_run(actions,extra_env={'DILNA_SMTP_TIMEOUT':'2','DILNA_SMTP_HOST':'127.0.0.1'})
if c.tk_no_error(r):
    for index in (5,6,7,8,9,10):
        widgets=r.widgets(index=index)
        c.add('Odezva a jediný přenos '+str(index),named(r,'stav',index).get('text')==pending
              and all(w['state']=='disabled' for w in widgets if w['kind'] in ('button','radiobutton') and w['text']!='Zkontrolovat záchyt')
              and all(w['state']!='disabled' for w in widgets if w['kind']=='entry')
              and named(r,'nahled',index).get('state')=='disabled' and 'Předmět: Původní snímek' in named(r,'nahled',index).get('value',''),
              'SMTP nesmí blokovat Tk ani vyvolat druhý přenos. Formulář lze měnit, odesílaný snímek zůstává stejný.')
    c.add('Zachycený původní snímek','Zachyceno: 1 | poslední předmět: Původní snímek'==named(r,'zachyt',11).get('text')
          and named(r,'predmet',11).get('value')=='Nový koncept' and named(r,'telo',11).get('value')=='Další práce\n', 'Výsledek nepřepisuje pozdější práci v polích.')
    c.add('Odmítnutí a ruční nový pokus',named(r,'stav',14).get('text')=='Příjemce byl odmítnut. Zpráva nebyla převzata.'
          and named(r,'zachyt',14).get('text','').startswith('Zachyceno: 1')
          and named(r,'stav',17).get('text')=='Zprávu převzal místní záchyt.'
          and named(r,'zachyt',17).get('text')=='Zachyceno: 2 | poslední předmět: Nový koncept', 'Nový ruční pokus načte aktuální pole; odmítnutí nevymaže formulář.')
    c.add('SMTP je mimo hlavní smyčku',all(row['ms']<250 for row in r.callbacks or []),'Spusťte pracovníka, nevolejte přenos přímo z callbacku.')
short=c.tk_run(form+[click('Opožděné potvrzení'),click(send),wait,click(send),{'action':'wait','ms':400},click('Zkontrolovat záchyt')],
               extra_env={'DILNA_SMTP_TIMEOUT':'0.05','DILNA_SMTP_HOST':'127.0.0.1'})
if c.tk_no_error(short,'Nejistý přenos zůstane řízený uživatelem'):
    c.add('Kontrola před novým pokusem',named(short,'stav',6).get('text')=='Přenos není potvrzený. Před novým pokusem zkontrolujte záchyt.'
          and named(short,'stav',7).get('text')=='Nejprve zkontrolujte záchyt před dalším pokusem.'
          and named(short,'zachyt',9).get('text','').startswith('Zachyceno: 1')
          and named(short,'stav',9).get('text')=='Záchyt zkontrolován. Další pokus může vytvořit kopii zprávy.', 'Po nejistém potvrzení nový přenos vyžaduje ruční kontrolu; nevytvářejte automatickou kopii.')
c.done()
