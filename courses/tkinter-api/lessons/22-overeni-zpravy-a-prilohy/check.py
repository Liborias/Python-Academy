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

from copy import deepcopy
from email.message import EmailMessage
valid={"prijemce":"  jan@example.test ","predmet":"  Český předmět  ","text":"  Dobrý den.\n.Řádek\n","priloha":""}
path=work/"česká příloha.txt";data="Žofie\n".encode("utf-8");path.write_bytes(data)
large=work/"velky.bin";large.write_bytes(b"x"*1_000_001)
if ns:
    for attachment in ["",str(path)]:
        model=dict(valid,priloha=attachment);before=deepcopy(model)
        ok,msg=c.call(ns,"sestav_zpravu",(model,))
        good=ok and isinstance(msg,EmailMessage)
        if good:
            parts=list(msg.iter_attachments())
            good=str(msg['To'])=='jan@example.test' and str(msg['Subject'])=='Český předmět' and str(msg['From'])=='eva@example.test'
            body=msg.get_body(preferencelist=('plain',))
            good=good and body is not None and body.get_content()==valid['text'] and model==before
            good=good and (len(parts)==1 and parts[0].get_payload(decode=True)==data and parts[0].get_filename()==path.name if attachment else not parts)
        c.add("Ověřená samostatná zpráva "+attachment,good,"Vraťte EmailMessage s aktuálními hlavičkami, tělem a přesnými bajty přílohy. Koncept neměňte.")
        if ok and isinstance(msg,EmailMessage):
            model['predmet']='Pozdější změna';path.write_bytes(b'pozdeji')
            snapshot_parts=list(msg.iter_attachments())
            c.add("Zpráva je snímek konceptu",str(msg['Subject'])=='Český předmět' and (not attachment or len(snapshot_parts)==1 and snapshot_parts[0].get_payload(decode=True)==data),"Hotová zpráva už nečte formulář ani cestu přílohy.")
            path.write_bytes(data)
    bad=[(dict(valid,prijemce='chyba'), 'prijemce'),(dict(valid,prijemce='a@example.test\nBcc: x@example.test'),'prijemce'),
         (dict(valid,predmet='  '),'predmet'),(dict(valid,predmet='A\nB'),'predmet'),(dict(valid,text=' \n'),'text'),
         (dict(valid,priloha=str(work/'chybi.txt')),'priloha'),(dict(valid,priloha=str(large)),'priloha'),
         (dict(valid,text=None),'koncept'),({},'koncept')]
    for i,(model,field) in enumerate(bad):
        before=deepcopy(model);ok,error=c.call(ns,'sestav_zpravu',(model,))
        c.add('Chyba konkrétního pole '+str(i),not ok and isinstance(error,ValueError) and getattr(error,'pole',None)==field and model==before,
              'Vyvolejte ChybaPole se správným pole; neplatný koncept ani přílohu neměňte.')

steps=[];expected=[];dialogs=[]
def step(action,status=None,field=None,preview=None,file=None,fields=None):
    steps.append(action);expected.append((len(steps),status,field,preview,file,fields))
step(click('Ověřit a zobrazit'),'Příjemce: zadejte jednu platnou adresu.','prijemce')
step(fill('prijemce','  jan@example.test '))
step(click('Ověřit a zobrazit'),'Předmět: napište neprázdný text bez nového řádku.','predmet')
step(fill('predmet','  Český předmět  '))
step(click('Ověřit a zobrazit'),'Text: napište tělo zprávy.','telo')
step(fill('telo',valid['text']))
step(click('Ověřit a zobrazit'),'Zpráva je připravená. Nic se neodeslalo.',preview='Předmět: Český předmět')
for chosen,message in [(str(path),'Příloha vybrána. Obnovte náhled.'),('','Výběr přílohy zrušen.'),
                       (str(work/'chybi.txt'),'Příloha: soubor nelze načíst nebo překračuje 1 000 000 B.')]:
    dialogs.append({'kind':'open','path':chosen});step(click('Vybrat přílohu'),message,file='Příloha: '+path.name)
step(click('Ověřit a zobrazit'),'Zpráva je připravená. Nic se neodeslalo.',preview='Příloha: '+path.name)
step(fill('prijemce','chyba'))
step(click('Ověřit a zobrazit'),'Příjemce: zadejte jednu platnou adresu.','prijemce',preview='Zpráva zatím není připravená.')
step(click('Odebrat přílohu'),'Příloha odebrána. Obnovte náhled.',file='Bez přílohy.')
r=c.tk_run(steps,dialogs=dialogs)
if c.tk_no_error(r):
    for index,status,field,preview,file,fields in expected:
        ok=(status is None or named(r,'stav',index).get('text')==status)
        ok=ok and (not field or named(r,field if field!='text' else 'telo',index).get('focused'))
        ok=ok and (not preview or preview in named(r,'nahled',index).get('value',''))
        ok=ok and (not file or named(r,'soubor',index).get('text')==file) and named(r,'nahled',index).get('state')=='disabled'
        if index>=6:ok=ok and named(r,'telo',index).get('value')==valid['text']
        c.add('Ověření a zachování polí '+str(index),ok,'Chyba ukáže pole a fokus, zrušení i neúspěšný výběr zachová přílohu i rozepsaný text.')
    c.add('Zrušení a chyba nemění předchozí náhled',named(r,'nahled',8).get('value')==named(r,'nahled',9).get('value')==named(r,'nahled',10).get('value'), 'Při zrušeném nebo chybném výběru nic nenahrazujte.')
c.done()
