import sys
from pathlib import Path
from unittest.mock import patch
import tkinter
from dilna_check import check

c=check();sys.path.insert(0,str(c.student.parent))
with patch.object(tkinter,'Tk',side_effect=RuntimeError('Import nesmí otevřít okno.')):ns=c.load()
work=c.student.parent
files=[]
for name,data,content_type in [('česká poznámka.txt','Žofie\nDruhý řádek.\n'.encode('utf-8'),'text/plain'),('obsah.neznamytypabc',b'\x00\xff\x01','application/octet-stream'),('prazdny.txt',b'','text/plain'),('zabaleno.txt.gz',b'cvicebni data','application/octet-stream')]:
    path=work/name;path.write_bytes(data);files.append((path,data,content_type))
large=work/'velky.bin';large.write_bytes(b'x'*1_000_001)
if ns and callable(ns.get('pridej_prilohu')):
    for i,(path,data,content_type) in enumerate(files):
        msg=ns['vytvor_zpravu']('eva@example.test','jan@example.test','Příloha','České tělo')
        ok,value=c.call(ns,'pridej_prilohu',(msg,str(path)))
        attachments=list(msg.iter_attachments());body=msg.get_body(preferencelist=('plain',))
        c.add('Původní zpráva a příloha '+str(i),ok and value is msg and len(attachments)==1
              and attachments[0].get_filename()==path.name and attachments[0].get_content_type()==content_type
              and attachments[0].get_payload(decode=True)==data and body is not None and body.get_content()=='České tělo\n'
              and str(msg['Subject'])=='Příloha','Přidejte přesné bytes, správný typ a samotný název, zachovejte tělo i hlavičky.')
    for i,(path,error) in enumerate([(work/'chybi.txt',OSError),(work,OSError),(large,ValueError)]):
        msg=ns['vytvor_zpravu']('eva@example.test','jan@example.test','Beze změny','Původní tělo')
        msg.add_attachment(b'puvodni',maintype='application',subtype='octet-stream',filename='puvodni.bin')
        before=msg.as_bytes();ok,value=c.call(ns,'pridej_prilohu',(msg,str(path)))
        c.add('Chyba zachová zprávu '+str(i),not ok and isinstance(value,error) and msg.as_bytes()==before,'Načtení a limit ověřte před změnou zprávy.')

paths=['',str(files[0][0]),'',str(work/'chybi.txt'),str(large),str(files[1][0])]
r=c.tk_run([{'action':'click','text':'Vybrat přílohu'} for _ in paths],dialogs=[{'kind':'open','path':p} for p in paths])
if c.tk_no_error(r):
    text=r.widgets('text');labels=r.widgets('label')
    initial='Příloha zatím není vybraná.';status='Zpráva se pouze připravuje, nic se neodesílá.'
    file_labels=[w for w in labels if w['text']==initial];status_labels=[w for w in labels if w['text']==status]
    expected=[(initial,status),(initial,'Výběr přílohy zrušen.')]
    chosen=f'Příloha: {files[0][0].name} | text/plain | {len(files[0][1])} B'
    expected += [(chosen,'Příloha je připravená. Zpráva nebyla odeslána.'),(chosen,'Výběr přílohy zrušen.'),(chosen,'Soubor nelze přiložit.'),(chosen,'Soubor nelze přiložit.'),
                 (f'Příloha: {files[1][0].name} | application/octet-stream | 3 B','Příloha je připravená. Zpráva nebyla odeslána.')]
    for i,(filename,message) in enumerate(expected):
        by_id={w['id']:w for w in r.widgets(index=i)};texts=r.widgets('text',i)
        ok=len(file_labels)==len(status_labels)==len(texts)==len(text)==1
        ok=ok and by_id.get(file_labels[0]['id'],{}).get('text')==filename and by_id.get(status_labels[0]['id'],{}).get('text')==message
        ok=ok and texts[0]['state']=='disabled' and texts[0]['value']==text[0]['value'] and 'Předmět: Poznámky z Pythonu' in texts[0]['value']
        ok=ok and len(r.widgets(index=i))==len(r.widgets()) and all(w['visible'] for w in r.widgets(index=i))
        c.add('Výběr a zachování náhledu '+str(i),ok,'Zrušení a chyba zachovají předchozí výběr, nový úspěch přílohu nahradí. Náhled zůstane pouze pro čtení.')
c.done()
