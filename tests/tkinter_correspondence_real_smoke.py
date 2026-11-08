"""Skutečné Tk a SMTP pro projekt 21–24; volba cest dialogů je řízená testem."""
import argparse
from contextlib import contextmanager
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from unittest.mock import patch

ROOT=Path(__file__).resolve().parent.parent
IDS={21:'21-koncept-a-formular',22:'22-overeni-zpravy-a-prilohy',23:'23-predani-snimku-na-pozadi',24:'24-projekt-korespondencni-dilna'}
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--lesson',type=int,choices=IDS)
p.add_argument('--short-timeout',action='store_true')
p.add_argument('--shots',type=Path)
a=p.parse_args()
if not os.environ.get('DISPLAY'):raise SystemExit('Nastavte DISPLAY na grafickou plochu.')
if a.lesson is None:
    for lesson,short in [(21,False),(22,False),(23,False),(24,False),(23,True),(24,True)]:
        command=[sys.executable,__file__,'--lesson',str(lesson)]
        if short:command.append('--short-timeout')
        if a.shots:command+=['--shots',str(a.shots)]
        result=subprocess.run(command,capture_output=True,text=True,timeout=15)
        if result.returncode:raise SystemExit(result.stdout+result.stderr)
        print(result.stdout.strip())
    raise SystemExit(0)

import tkinter as tk
from tkinter import ttk,filedialog
from email.parser import BytesParser
from email.policy import default
failures=[];entered=[];beats=[];captures=[];calls=[]
main_id=threading.get_ident();active=0;maximum=0;lock=threading.Lock()
original_loop=tk.Tk.mainloop

def mainloop(root,*args,**kwargs):
    entered.append(root);closed=False
    def stop():
        nonlocal closed
        if not closed:closed=True;root.destroy()
    def fail(error):failures.append(error);stop()
    root.report_callback_exception=lambda cls,error,tb:fail(error)
    def beat():beats.append(time.monotonic());root.after(10,beat)
    root.after(1,beat)
    def finish():
        if a.lesson>=23:
            assert len(calls)==(1 if a.short_timeout else 3),calls
            assert maximum==1 and all(c['thread']!=main_id for c in calls),calls
            assert len(beats)>2 and max(y-x for x,y in zip(beats,beats[1:]))<.25,'Hlavní smyčka čeká na SMTP'
        root.update_idletasks()
        if a.shots:
            a.shots.mkdir(parents=True,exist_ok=True)
            target=a.shots/(f'project-real-{a.lesson}'+('-timeout' if a.short_timeout else '')+'.png')
            script='from PIL import ImageGrab; import os,sys; ImageGrab.grab(xdisplay=os.environ["DISPLAY"]).save(sys.argv[1])'
            subprocess.run(['python3','-c',script,str(target)],check=True,timeout=5)
        stop()
    def setup():
        try:
            root.focus_force()
            def walk(widget):
                yield widget
                for child in widget.winfo_children():yield from walk(child)
            widgets=list(walk(root))
            named={w.winfo_name():w for w in widgets}
            buttons={w.cget('text'):w for w in widgets if isinstance(w,(ttk.Button,ttk.Radiobutton))}
            steps=[]
            def action(f):steps.append(('action',f))
            def check(f,msg):
                def verify():
                    if not f():raise AssertionError(msg)
                action(verify)
            def fill(name,text):
                w=named[name]
                def write():
                    w.delete('1.0' if isinstance(w,tk.Text) else 0,'end')
                    w.insert('1.0' if isinstance(w,tk.Text) else 0,text)
                action(write)
            def click(text):action(lambda:buttons[text].invoke())
            def value(name):
                w=named[name]
                return w.get('1.0','end-1c') if isinstance(w,tk.Text) else w.get()
            def label(name):return named[name].cget('text')
            def idle():steps.append(('wait',lambda:not buttons['Předat místnímu záchytu'].instate(['disabled'])))
            def form(subject='Původní snímek',body='Původní text\n'):
                fill('prijemce','jan@example.test');fill('predmet',subject);fill('telo',body)
            if a.lesson==21:
                form('  Žofie  ',' A\nB\n');click('Obnovit náhled')
                check(lambda:value('nahled')=='Komu: jan@example.test\nPředmět:   Žofie  \n\n A\nB\n','Přesné řádky konceptu')
                fill('prijemce','jan@');fill('predmet','');click('Obnovit náhled')
                check(lambda:value('prijemce')=='jan@' and value('predmet')=='' and 'Komu: jan@' in value('nahled'),'Nedopsaný koncept')
                action(finish)
            else:
                path=Path.cwd()/'česká příloha.txt';original='Žofie\n'.encode('utf-8');path.write_bytes(original)
                large=Path.cwd()/'velky.bin';large.write_bytes(b'x'*1_000_001)
                click('Ověřit a zobrazit')
                check(lambda:label('stav')=='Příjemce: zadejte jednu platnou adresu.' and root.focus_get() is named['prijemce'],'Adresní chyba a fokus')
                form();click('Vybrat přílohu');click('Ověřit a zobrazit')
                check(lambda:'Příloha: česká příloha.txt' in value('nahled') and str(named['nahled'].cget('state'))=='disabled','Příloha v náhledu')
                before=[];action(lambda:before.append(value('nahled')))
                for message in ['Výběr přílohy zrušen.','Příloha: soubor nelze načíst nebo překračuje 1 000 000 B.','Příloha: soubor nelze načíst nebo překračuje 1 000 000 B.']:
                    click('Vybrat přílohu')
                    check(lambda message=message:label('stav')==message and label('soubor')=='Příloha: česká příloha.txt' and value('nahled')==before[0],'Chyba nebo zrušení zachová přílohu')
                if a.lesson==24:
                    click('Uložit koncept');fill('predmet','Změněno');click('Načíst koncept')
                    check(lambda:value('predmet')=='Původní snímek' and value('telo')=='Původní text\n' and label('soubor')=='Příloha: česká příloha.txt','Celý uložený koncept')
                    click('Ověřit a zobrazit');action(lambda:before.__setitem__(0,value('nahled')))
                    for expected in ['Načítání zrušeno.','Koncept se nepodařilo načíst.']:
                        click('Načíst koncept')
                        check(lambda expected=expected:label('stav')==expected and value('nahled')==before[0] and value('telo')=='Původní text\n','Neúspěšné načtení zachová práci')
                if a.lesson==22:action(finish)
                else:
                    send='Předat místnímu záchytu';click('Opožděné potvrzení');click(send);click(send)
                    fill('prijemce','dalsi@example.test');fill('predmet','Novější práce');fill('telo','Další text\n')
                    action(lambda:path.write_bytes(b'jine bajty'))
                    if a.short_timeout:
                        idle()
                        check(lambda:label('stav')=='Přenos není potvrzený. Před novým pokusem zkontrolujte záchyt.','Nejistý výsledek')
                        if a.lesson==24:
                            click('Načíst koncept')
                            check(lambda:value('predmet')=='Původní snímek','Načtení po nejistém přenosu')
                        click(send)
                        check(lambda:label('stav')=='Nejprve zkontrolujte záchyt před dalším pokusem.','Načtení neobejde kontrolu záchytu')
                        steps.append(('delay',450));click('Zkontrolovat záchyt')
                        check(lambda:len(captures[0].zpravy)==1 and label('stav')=='Záchyt zkontrolován. Další pokus může vytvořit kopii zprávy.','Žádný automatický druhý přenos')
                    else:
                        steps.append(('wait',lambda:len(captures[0].zpravy)==1))
                        click('Zkontrolovat záchyt')
                        check(lambda:label('stav')=='Předávám zprávu místnímu záchytu...' and label('zachyt').startswith('Zachyceno: 1'),'Použitelné okno při skutečném SMTP čekání')
                        idle()
                        check(lambda:value('predmet')=='Novější práce' and value('telo')=='Další text\n','Dokončení přenosu zachová novou práci')
                        click('Odmítnutí příjemce');click(send);idle()
                        check(lambda:len(captures[0].zpravy)==1 and label('stav')=='Příjemce byl odmítnut. Zpráva nebyla převzata.','Odmítnutí bez změny formuláře')
                        click('Přijetí');click(send);idle()
                        check(lambda:len(captures[0].zpravy)==2 and label('stav')=='Zprávu převzal místní záchyt.','Ruční nový pokus')
                    def verify_capture():
                        record=captures[0].zpravy[0];msg=BytesParser(policy=default).parsebytes(record.data)
                        assert record.prijemci==('jan@example.test',) and str(msg['Subject'])=='Původní snímek'
                        assert msg.get_body(preferencelist=('plain',)).get_content().replace('\r\n','\n')=='Původní text\n'
                        part=list(msg.iter_attachments())[0]
                        assert part.get_filename()==path.name and part.get_payload(decode=True)==original
                        if not a.short_timeout:
                            record=captures[0].zpravy[-1];msg=BytesParser(policy=default).parsebytes(record.data)
                            assert record.prijemci==('dalsi@example.test',) and str(msg['Subject'])=='Novější práce'
                            assert list(msg.iter_attachments())[0].get_payload(decode=True)==b'jine bajty'
                    action(verify_capture);action(finish)
            position=0;deadline=0
            def advance():
                nonlocal position,deadline
                try:
                    if position>=len(steps):return
                    kind,f=steps[position]
                    if kind=='wait':
                        if not deadline:deadline=time.monotonic()+3
                        if not f():
                            if time.monotonic()>deadline:raise AssertionError('Čekání na SMTP stav')
                            root.after(10,advance);return
                        deadline=0
                    elif kind=='delay':position+=1;root.after(f,advance);return
                    else:f()
                    position+=1
                    if not closed:root.after(1,advance)
                except BaseException as error:fail(error)
            advance()
        except BaseException as error:fail(error)
    root.after(40,setup);root.after(8000,lambda:fail(AssertionError('Limit skutečného GUI testu')))
    return original_loop(root,*args,**kwargs)

with tempfile.TemporaryDirectory() as temp:
    work=Path(temp)
    for f in (ROOT/'courses/tkinter-api/lessons'/IDS[a.lesson]/'files').glob('*'):
        if f.is_file():shutil.copy2(f,work/f.name)
    os.chdir(work);sys.path.insert(0,str(work))
    if a.lesson>=23:
        for key in ['DILNA_SMTP_HOST','DILNA_SMTP_PORT','DILNA_SMTP_TIMEOUT']:os.environ.pop(key,None)
        os.environ['DILNA_SMTP_TIMEOUT']='0.05' if a.short_timeout else '2'
        import cvicna_posta,odesilani
        original_capture=cvicna_posta.cvicna_posta;original_client=odesilani.odesli_do_zachytu
        @contextmanager
        def capture():
            with original_capture() as server:captures.append(server);yield server
        cvicna_posta.cvicna_posta=capture
        def client(msg,host,port,timeout=2):
            global active,maximum
            with lock:calls.append({'thread':threading.get_ident()});active+=1;maximum=max(maximum,active)
            try:return original_client(msg,host,port,timeout)
            finally:
                with lock:active-=1
        odesilani.odesli_do_zachytu=client
    choices=[str(work/'česká příloha.txt'),'',str(work/'chybi.txt'),str(work/'velky.bin')]
    if a.lesson==24:
        broken=work/'rozbity.json';broken.write_text('{',encoding='utf-8')
        choices += [str(work/'koncept.json'),'',str(broken)]
        if a.short_timeout:choices += [str(work/'koncept.json')]
    tk.Tk.mainloop=mainloop
    try:
        with patch.object(filedialog,'askopenfilename',side_effect=choices),patch.object(filedialog,'asksaveasfilename',return_value=str(work/'koncept.json')):
            runpy.run_path(str(ROOT/'courses/tkinter-api/lessons'/IDS[a.lesson]/'example.py'),run_name='__main__')
        assert len(entered)==1 and not failures,failures
        print(f'OK: skutečné Tk {tk.TkVersion}, projekt {a.lesson}, '+('nejisté SMTP' if a.short_timeout else 'běžný průchod'))
    finally:tk.Tk.mainloop=original_loop
