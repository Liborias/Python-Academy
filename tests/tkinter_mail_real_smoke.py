"""Skutečné Tk + místní SMTP/přílohy pro 19/20; DISPLAY=:... python tento_soubor.py."""
import argparse
from contextlib import contextmanager
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parent.parent
IDS={19:'19-prilohy-a-vyber-souboru',20:'20-nastaveni-smtp-a-chyby'}
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--lesson',type=int,choices=IDS)
p.add_argument('--short-timeout',action='store_true')
p.add_argument('--shots',type=Path)
a=p.parse_args()
if not os.environ.get('DISPLAY'):raise SystemExit('Nastavte DISPLAY na grafickou plochu.')
if a.lesson is None:
    for index,short in [(19,False),(20,False),(20,True)]:
        command=[sys.executable,__file__,'--lesson',str(index)]
        if short:command.append('--short-timeout')
        if a.shots:command+=['--shots',str(a.shots)]
        r=subprocess.run(command,capture_output=True,text=True,timeout=15)
        if r.returncode:raise SystemExit(r.stdout+r.stderr)
        print(r.stdout.strip())
    raise SystemExit(0)

import tkinter as tk
from tkinter import ttk,filedialog
main_id=threading.get_ident();calls=[];active=0;maximum=0;lock=threading.Lock()
failures=[];entered=[];beats=[];captures=[]
original_loop=tk.Tk.mainloop

def mainloop(root,*args,**kwargs):
    entered.append(root);closed=[False]
    def stop():
        if not closed[0]:closed[0]=True;root.destroy()
    def fail(error):failures.append(error);stop()
    root.report_callback_exception=lambda cls,error,tb:fail(error)
    def beat():beats.append(time.monotonic());root.after(10,beat)
    root.after(1,beat)
    def finish():
        assert not failures,failures
        if a.lesson==20:
            assert len(calls)==(1 if a.short_timeout else 3),calls
            assert all(c['thread']!=main_id and c['host']=='127.0.0.1' and c['port']==captures[0].port for c in calls),calls
            assert maximum==1,maximum
        if a.lesson==20:
            assert len(beats)>2 and max(y-x for x,y in zip(beats,beats[1:]))<.25,'Zablokovaná hlavní smyčka'
        root.update_idletasks()
        if a.shots:
            a.shots.mkdir(parents=True,exist_ok=True)
            name=f'mail-real-{a.lesson}'+('-timeout' if a.short_timeout else '')+'.png'
            code='from PIL import ImageGrab; import os,sys; ImageGrab.grab(xdisplay=os.environ["DISPLAY"]).save(sys.argv[1])'
            subprocess.run(['python3','-c',code,str(a.shots/name)],check=True,timeout=5)
        stop()
    def setup():
        try:
            children=root.winfo_children()
            buttons={w.cget('text'):w for w in children if isinstance(w,ttk.Button)}
            radios={w.cget('text'):w for w in children if isinstance(w,ttk.Radiobutton)}
            labels=[w for w in children if isinstance(w,ttk.Label)]
            text=next(w for w in children if isinstance(w,tk.Text))
            texts=lambda:[w.cget('text') for w in labels]
            if a.lesson==19:
                folder=Path.cwd();first=folder/'česká příloha.txt';data='Žofie\n'.encode('utf-8');first.write_bytes(data)
                second=folder/'obsah.neznamytypabc';second.write_bytes(b'\x00\xff\x01')
                large=folder/'velky.bin';large.write_bytes(b'x'*1_000_001)
                status=next(w for w in labels if w.cget('text').startswith('Zpráva se'))
                filename=next(w for w in labels if w.cget('text').startswith('Příloha'))
                original=text.get('1.0','end-1c')
                with patch.object(filedialog,'askopenfilename',side_effect=[str(first),'',str(folder/'chybi.txt'),str(large),str(second)]):
                    buttons['Vybrat přílohu'].invoke()
                    assert filename.cget('text')==f'Příloha: {first.name} | text/plain | {len(data)} B'
                    before=filename.cget('text')
                    for expected in ['Výběr přílohy zrušen.','Soubor nelze přiložit.','Soubor nelze přiložit.']:
                        buttons['Vybrat přílohu'].invoke()
                        assert filename.cget('text')==before and status.cget('text')==expected
                        assert text.get('1.0','end-1c')==original
                    buttons['Vybrat přílohu'].invoke()
                    assert filename.cget('text')==f'Příloha: {second.name} | application/octet-stream | 3 B'
                    assert text.get('1.0','end-1c')==original and str(text.cget('state'))=='disabled'
                finish();return
            send='Předat místnímu záchytu';steps=[]
            def action(f):steps.append(('action',f))
            def check(f,message):
                def verify():
                    if not f():raise AssertionError(message+': '+repr(texts()))
                action(verify)
            def click(name):action(lambda:buttons[name].invoke())
            def radio(name):action(lambda:radios[name].invoke())
            def wait(f):steps.append(('wait',f))
            def idle():wait(lambda:not buttons[send].instate(['disabled']))
            def delay(ms):steps.append(('delay',ms))
            check(lambda:'Zachyceno: 0' in texts(),'Počáteční záchyt')
            radio('Opožděné potvrzení');click(send)
            if a.short_timeout:
                idle()
                check(lambda:'Přenos není potvrzený. Před novým pokusem zkontrolujte záchyt.' in texts(),'Nejistý výsledek')
                delay(450);click('Zkontrolovat záchyt')
                check(lambda:'Zachyceno: 1' in texts() and 'Předmět: Zkouška nastavení' in text.get('1.0','end-1c'),'Převzetí před timeoutem bez opakování')
            else:
                click(send);radio('Odmítnutí příjemce')
                wait(lambda:len(captures[0].zpravy)==1)
                click('Zkontrolovat záchyt')
                check(lambda:'Předávám zprávu místnímu záchytu...' in texts() and 'Zachyceno: 1' in texts() and buttons[send].instate(['disabled']),'Odezva během SMTP čekání')
                idle();check(lambda:'Zprávu převzal místní záchyt.' in texts(),'Potvrzené přijetí')
                radio('Odmítnutí příjemce');click(send);idle()
                check(lambda:'Příjemce byl odmítnut. Zpráva nebyla převzata.' in texts() and 'Zachyceno: 1' in texts(),'Odmítnutí RCPT bez další zprávy')
                radio('Přijetí');click(send);idle()
                check(lambda:'Zprávu převzal místní záchyt.' in texts() and 'Zachyceno: 2' in texts(),'Nový ruční pokus')
            check(lambda:str(text.cget('state'))=='disabled','Náhled pouze pro čtení')
            steps.append(('action',finish));position=0;deadline=0
            def advance():
                nonlocal position,deadline
                try:
                    if position>=len(steps):return
                    kind,value=steps[position]
                    if kind=='wait':
                        if not deadline:deadline=time.monotonic()+3
                        if not value():
                            if time.monotonic()>deadline:raise AssertionError('Nedokončený SMTP krok')
                            root.after(10,advance);return
                        deadline=0
                    elif kind=='delay':position+=1;root.after(value,advance);return
                    else:value()
                    position+=1
                    if not closed[0]:root.after(1,advance)
                except BaseException as error:fail(error)
            advance()
        except BaseException as error:fail(error)
    root.after(30,setup);root.after(7000,lambda:fail(AssertionError('Celkový limit GUI testu')))
    return original_loop(root,*args,**kwargs)

with tempfile.TemporaryDirectory() as folder:
    work=Path(folder)
    for file in (ROOT/'courses/tkinter-api/lessons'/IDS[a.lesson]/'files').glob('*'):
        if file.is_file():shutil.copy2(file,work/file.name)
    os.chdir(work);sys.path.insert(0,str(work))
    if a.lesson==20:
        for key in ['DILNA_SMTP_HOST','DILNA_SMTP_PORT','DILNA_SMTP_TIMEOUT']:os.environ.pop(key,None)
        os.environ['DILNA_SMTP_TIMEOUT']='0.05' if a.short_timeout else '2'
        import cvicna_posta,odesilani
        original_capture=cvicna_posta.cvicna_posta;original_client=odesilani.odesli_do_zachytu
        @contextmanager
        def capture():
            with original_capture() as server:
                captures.append(server);yield server
        cvicna_posta.cvicna_posta=capture
        def client(msg,host,port,timeout=2):
            global active,maximum
            with lock:
                calls.append({'thread':threading.get_ident(),'host':host,'port':port});active+=1;maximum=max(maximum,active)
            try:return original_client(msg,host,port,timeout)
            finally:
                with lock:active-=1
        odesilani.odesli_do_zachytu=client
    tk.Tk.mainloop=mainloop
    try:
        runpy.run_path(str(ROOT/'courses/tkinter-api/lessons'/IDS[a.lesson]/'example.py'),run_name='__main__')
        assert len(entered)==1 and not failures,failures
        mode='timeout' if a.short_timeout else 'běžný průchod'
        print(f'OK: skutečné Tk {tk.TkVersion}, lekce {a.lesson}, {mode}, přílohy/místní SMTP')
    finally:tk.Tk.mainloop=original_loop
