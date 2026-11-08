"""Skutečné finální Tk: zdroje z jiného cwd, klávesy před třídní vazbou a místní SMTP."""
import argparse
from contextlib import contextmanager
import json
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
IDS={27:'27-cesty-a-klavesove-zkratky',28:'28-predani-a-zaverecne-overeni'}
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--lesson',type=int,choices=IDS);p.add_argument('--short-timeout',action='store_true');p.add_argument('--shots',type=Path);a=p.parse_args()
if not os.environ.get('DISPLAY'):raise SystemExit('Nastavte DISPLAY na grafickou plochu.')
if a.lesson is None:
    for lesson,short in [(27,False),(28,False),(27,True),(28,True)]:
        cmd=[sys.executable,__file__,'--lesson',str(lesson)]
        if short:cmd.append('--short-timeout')
        if a.shots:cmd+=['--shots',str(a.shots)]
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=15)
        if r.returncode:raise SystemExit(r.stdout+r.stderr)
        print(r.stdout.strip())
    raise SystemExit(0)

import tkinter as tk
from tkinter import ttk,filedialog
from email.parser import BytesParser
from email.policy import default
failures=[];beats=[];captures=[];calls=[];main_id=threading.get_ident()
original_loop=tk.Tk.mainloop

def mainloop(root,*args,**kwargs):
    closed=False
    def stop():
        nonlocal closed
        if not closed:closed=True;root.destroy()
    def fail(error):failures.append(error);stop()
    root.report_callback_exception=lambda cls,error,tb:fail(error)
    def beat():beats.append(time.monotonic());root.after(10,beat)
    root.after(1,beat)
    def setup():
        try:
            root.focus_force()
            def walk(w):
                yield w
                for child in w.winfo_children():yield from walk(child)
            widgets=list(walk(root));named={w.winfo_name():w for w in widgets}
            buttons={w.cget('text'):w for w in widgets if isinstance(w,(ttk.Button,ttk.Radiobutton))}
            steps=[]
            def action(f):steps.append(('action',f))
            def check(f,label):
                def verify():
                    if not f():raise AssertionError(label)
                action(verify)
            def click(text):action(lambda:buttons[text].invoke())
            def fill(name,text):
                w=named[name]
                def write():w.delete('1.0' if isinstance(w,tk.Text) else 0,'end');w.insert('1.0' if isinstance(w,tk.Text) else 0,text)
                action(write)
            def value(name):
                w=named[name];return w.get('1.0','end-1c') if isinstance(w,tk.Text) else w.get()
            def status():return named['stav'].cget('text')
            def focus():named['telo'].focus_force()
            def key(sequence):
                def press():focus();named['telo'].event_generate(sequence)
                action(press)
            send='Předat místnímu záchytu'
            def idle():steps.append(('wait',lambda:not buttons[send].instate(['disabled'])))
            click('Načíst ukázku')
            check(lambda:value('predmet')=='Pozdrav z dokončené dílny','Zdroj vedle __file__ z jiného cwd')
            fill('predmet','Původní snímek');fill('telo',' A\nB\n');click('Vybrat přílohu')
            key('<Control-Return>');key('<Control-s>')
            check(lambda:status()=='Koncept uložen. Nejde o potvrzení přenosu.' and value('telo')==' A\nB\n','Ctrl+S z těla')
            fill('predmet','Změna');fill('telo','Přepsáno');key('<Control-o>')
            check(lambda:value('predmet')=='Původní snímek' and value('telo')==' A\nB\n','Ctrl+O před třídní vazbou Text')
            before=[];key('<Control-Return>');action(lambda:before.append(value('nahled')))
            for message in ['Načítání zrušeno.','Koncept se nepodařilo načíst.']:
                key('<Control-o>');check(lambda message=message:status()==message and value('nahled')==before[0] and value('telo')==' A\nB\n','Chyba klávesového načtení zachová stav')
            asset=work/'data/vychozi-koncept.json';backup=asset.read_bytes()
            action(lambda:asset.unlink());click('Načíst ukázku')
            check(lambda:status()=='Ukázkový koncept není dostupný. Zkontrolujte složku data.' and value('nahled')==before[0],'Chyba zdroje zachová formulář')
            action(lambda:asset.write_bytes(backup))
            click('Opožděné potvrzení');click(send)
            fill('prijemce','dalsi@example.test');fill('predmet','Novější práce');fill('telo','Další text\n')
            action(lambda:attachment.write_bytes(b'jine bajty'))
            if a.short_timeout:
                idle();check(lambda:status()=='Přenos není potvrzený. Před novým pokusem zkontrolujte záchyt.','Nejisté potvrzení')
                key('<Control-o>');click(send)
                check(lambda:status()=='Nejprve zkontrolujte záchyt před dalším pokusem.','Načtení nemaže nutnou kontrolu')
                steps.append(('delay',450));click('Zkontrolovat záchyt')
            else:
                key('<Control-s>');key('<Control-o>');click('Načíst ukázku');click(send)
                steps.append(('wait',lambda:len(captures[0].zpravy)==1))
                click('Zkontrolovat záchyt')
                check(lambda:status()=='Předávám zprávu místnímu záchytu...','Odezva při SMTP čekání')
                idle();check(lambda:value('predmet')=='Novější práce' and value('telo')=='Další text\n','Dokončení zachová nové psaní')
                click('Odmítnutí příjemce');click(send);idle()
                check(lambda:status()=='Příjemce byl odmítnut. Zpráva nebyla převzata.' and len(captures[0].zpravy)==1,'Odmítnutí')
                click('Přijetí');click(send);idle()
            def finish():
                records=captures[0].zpravy
                assert len(calls)==(1 if a.short_timeout else 3) and all(t!=main_id for t in calls),calls
                assert len(records)==(1 if a.short_timeout else 2),records
                msg=BytesParser(policy=default).parsebytes(records[0].data)
                assert str(msg['Subject'])=='Původní snímek' and records[0].prijemci==('jan@example.test',)
                assert msg.get_body(preferencelist=('plain',)).get_content().replace('\r\n','\n')==' A\nB\n'
                assert list(msg.iter_attachments())[0].get_payload(decode=True)=='Žofie\n'.encode('utf-8')
                assert open_mock.call_count==(5 if a.short_timeout else 4),open_mock.call_count
                assert save_mock.call_count==1,save_mock.call_count
                assert max(y-x for x,y in zip(beats,beats[1:]))<.25,'Zablokovaná smyčka'
                root.update_idletasks()
                if a.shots:
                    a.shots.mkdir(parents=True,exist_ok=True)
                    shot=a.shots/(f'finish-real-{a.lesson}'+('-timeout' if a.short_timeout else '')+'.png')
                    script='from PIL import ImageGrab; import os,sys; ImageGrab.grab(xdisplay=os.environ["DISPLAY"]).save(sys.argv[1])'
                    subprocess.run(['python3','-c',script,str(shot)],check=True,timeout=5)
                stop()
            action(finish);position=0;deadline=0
            def advance():
                nonlocal position,deadline
                try:
                    if position>=len(steps):return
                    kind,f=steps[position]
                    if kind=='wait':
                        if not deadline:deadline=time.monotonic()+3
                        if not f():
                            if time.monotonic()>deadline:raise AssertionError('Čekání na stav')
                            root.after(10,advance);return
                        deadline=0
                    elif kind=='delay':position+=1;root.after(f,advance);return
                    else:f()
                    position+=1
                    if not closed:root.after(1,advance)
                except BaseException as error:fail(error)
            advance()
        except BaseException as error:fail(error)
    root.after(40,setup);root.after(8000,lambda:fail(AssertionError('Limit GUI testu')))
    return original_loop(root,*args,**kwargs)

with tempfile.TemporaryDirectory() as folder:
    work=Path(folder)/'projekt s mezerou';shutil.copytree(ROOT/'courses/tkinter-api/lessons'/IDS[a.lesson]/'files',work,ignore=shutil.ignore_patterns('__pycache__'))
    source=ROOT/'courses/tkinter-api/lessons'/IDS[27]/'solution.py' if a.lesson==27 else work/'aplikace.py'
    program=work/'overovana_aplikace.py';shutil.copy2(source,program)
    foreign=Path(folder)/'jine cwd';foreign.mkdir();os.chdir(foreign);sys.path.insert(0,str(work))
    attachment=work/'česká příloha.txt';attachment.write_bytes('Žofie\n'.encode('utf-8'))
    target=work/'moje-prace.json';broken=work/'vadny.json';broken.write_text('{',encoding='utf-8')
    for k in ['DILNA_SMTP_HOST','DILNA_SMTP_PORT','DILNA_SMTP_TIMEOUT']:os.environ.pop(k,None)
    os.environ['DILNA_SMTP_TIMEOUT']='0.05' if a.short_timeout else '2'
    import cvicna_posta,odesilani
    original_capture=cvicna_posta.cvicna_posta;original_client=odesilani.odesli_do_zachytu
    @contextmanager
    def capture():
        with original_capture() as server:captures.append(server);yield server
    cvicna_posta.cvicna_posta=capture
    def client(*args,**kwargs):calls.append(threading.get_ident());return original_client(*args,**kwargs)
    odesilani.odesli_do_zachytu=client
    choices=[str(attachment),str(target),'',str(broken)]
    if a.short_timeout:choices.append(str(target))
    tk.Tk.mainloop=mainloop
    try:
        with patch.object(filedialog,'askopenfilename',side_effect=choices) as open_mock,patch.object(filedialog,'asksaveasfilename',return_value=str(target)) as save_mock:
            runpy.run_path(str(program),run_name='__main__')
        assert not failures,failures
        print(f'OK: skutečné Tk {tk.TkVersion}, finální {a.lesson}, '+('nejisté SMTP' if a.short_timeout else 'klávesy, zdroje a SMTP'))
    finally:tk.Tk.mainloop=original_loop
