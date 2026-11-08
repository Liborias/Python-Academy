"""Skutečné Tk + skutečné místní HTTP pro lekce 15/16; vyžaduje DISPLAY."""
import argparse
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
IDS={15:'15-vlakno-fronta-a-after',16:'16-projekt-prevodnik-men'}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lesson',type=int,choices=IDS)
parser.add_argument('--shots',type=Path)
args=parser.parse_args()
if not os.environ.get('DISPLAY'):raise SystemExit('Nastavte DISPLAY na grafickou plochu.')
if args.lesson is None:
    for index in IDS:
        command=[sys.executable,__file__,'--lesson',str(index)]
        if args.shots:command += ['--shots',str(args.shots)]
        result=subprocess.run(command,capture_output=True,text=True,timeout=15)
        if result.returncode:raise SystemExit(result.stdout+result.stderr)
        print(result.stdout.strip())
    raise SystemExit(0)

import tkinter as tk
from tkinter import ttk
main_id=threading.get_ident();failures=[];entered=[];beats=[]
original_loop=tk.Tk.mainloop
request_log=[];inflight=0;maximum=0;lock=threading.Lock();flags={'fail_next':False}

def mainloop(root,*a,**kw):
    entered.append(root)
    closed=[False]
    def stop():
        if not closed[0]:
            closed[0]=True
            root.destroy()
    def fail(error):
        failures.append(error)
        stop()
    root.report_callback_exception=lambda cls,error,tb:fail(error)
    def heartbeat():
        beats.append(time.monotonic());root.after(10,heartbeat)
    root.after(1,heartbeat)
    def setup():
        try:
            widgets=root.winfo_children()
            buttons={w.cget('text'):w for w in widgets if isinstance(w,ttk.Button)}
            radios={w.cget('text'):w for w in widgets if isinstance(w,ttk.Radiobutton)}
            labels=[w for w in widgets if isinstance(w,ttk.Label)]
            texts=lambda:[w.cget('text') for w in labels]
            steps=[]
            def action(function):steps.append(('action',function))
            def check(condition,message):
                def verify():
                    if not condition():raise AssertionError(message+': '+repr(texts()))
                action(verify)
            def click(text):action(lambda:buttons[text].invoke())
            def radio(text):action(lambda:radios[text].invoke())
            def idle():steps.append(('wait',lambda:not buttons['Načíst kurz'].instate(['disabled'])))
            def delay(ms):steps.append(('delay',ms))
            if args.lesson==15:
                check(lambda:'Připraveno k načtení.' in texts(),'Počáteční stav')
                click('Načíst kurz');click('Načíst kurz');radio('Chyba serveru');click('Klikni během načítání')
                check(lambda:buttons['Načíst kurz'].instate(['disabled']) and 'Načítám kurz...' in texts(),'Běžící požadavek')
                delay(60)
                check(lambda:'Kliknutí: 1' in texts() and 'Načítám kurz...' in texts(),'Odezva při skutečně pomalém HTTP')
                click('Klikni během načítání');idle()
                check(lambda:'1 EUR = 25.00 CZK | 2026-01-15 | Cvičné API' in texts() and 'Kliknutí: 2' in texts(),'Výsledek a souběžné kliknutí')
                radio('Chyba serveru');click('Načíst kurz');idle()
                check(lambda:'Kurz se nepodařilo načíst. Zkuste to znovu.' in texts() and 'Kurz zatím není načtený.' in texts(),'HTTP 503')
                radio('Běžná odpověď');click('Načíst kurz');idle();click('Klikni během načítání')
                check(lambda:'Kurz načten.' in texts() and 'Kliknutí: 3' in texts(),'Nový pokus po chybě')
            else:
                entry=next(w for w in widgets if isinstance(w,ttk.Entry))
                def fill(value):
                    def update():entry.delete(0,tk.END);entry.insert(0,value)
                    action(update)
                check(lambda:buttons['Převést'].instate(['disabled']),'Převod čeká na kurz')
                fill('10');click('Načíst kurz');click('Načíst kurz');radio('USD');fill(' 1,5 ');delay(60)
                check(lambda:'Načítám kurz...' in texts() and entry.get()==' 1,5 ','Editace při načítání')
                idle();click('Převést')
                check(lambda:'Výsledek: 37.50 CZK' in texts(),'Aktuální částka v EUR')
                fill('-1');click('Převést')
                check(lambda:'Zadejte platnou nezápornou částku.' in texts() and 'Výsledek: zatím nic.' in texts(),'Chybná částka')
                fill('2');click('Převést');check(lambda:'Výsledek: 50.00 CZK' in texts(),'Oprava částky')
                radio('USD');check(lambda:buttons['Převést'].instate(['disabled']) and 'Kurz zatím není načtený.' in texts(),'Změna měny zneplatní kurz')
                click('Načíst kurz');idle();click('Převést')
                check(lambda:'Výsledek: 40.00 CZK' in texts() and '1 USD = 20.00 CZK | 2026-01-15 | Cvičné API' in texts(),'Kurz USD z API')
                radio('Cvičný soubor');click('Načíst kurz');idle();click('Převést')
                check(lambda:'Výsledek: 38.00 CZK' in texts() and '1 USD = 19.00 CZK | 2026-01-14 | Cvičný soubor' in texts(),'Alternativní soubor')
                radio('EUR');click('Načíst kurz');idle();click('Převést')
                check(lambda:'Výsledek: 48.00 CZK' in texts(),'Druhá měna ze souboru')
                action(lambda:flags.update(fail_next=True));radio('Cvičné API');click('Načíst kurz');idle()
                check(lambda:buttons['Převést'].instate(['disabled']) and 'Kurz zatím není načtený.' in texts(),'Skutečné HTTP 503 nesmí ponechat kurz')
                click('Načíst kurz');idle();click('Převést')
                check(lambda:'Výsledek: 50.00 CZK' in texts() and entry.get()=='2','Opakování po chybě')
            def finish():
                assert not failures,failures
                assert len(request_log)==(3 if args.lesson==15 else 4),request_log
                assert all(row['thread']!=main_id for row in request_log),request_log
                assert maximum==1,maximum
                assert max(b-a for a,b in zip(beats,beats[1:]))<.25,'Hlavní smyčka přestala reagovat'
                if args.shots:
                    args.shots.mkdir(parents=True,exist_ok=True);root.update_idletasks()
                    capture='from PIL import ImageGrab; import os,sys; ImageGrab.grab(xdisplay=os.environ["DISPLAY"]).save(sys.argv[1])'
                    subprocess.run(['python3','-c',capture,str(args.shots/f'tk-api-real-{args.lesson}.png')],check=True,timeout=5)
                stop()
            steps.append(('action',finish))
            position=0;deadline=0
            def advance():
                nonlocal position,deadline
                try:
                    if position>=len(steps):return
                    kind,value=steps[position]
                    if kind=='wait':
                        if not deadline:deadline=time.monotonic()+3
                        if not value():
                            if time.monotonic()>deadline:raise AssertionError('Nedokončené načítání')
                            root.after(10,advance);return
                        deadline=0
                    elif kind=='delay':
                        position+=1;root.after(value,advance);return
                    else:value()
                    position+=1
                    if not closed[0]:root.after(1,advance)
                except BaseException as error:fail(error)
            advance()
        except BaseException as error:fail(error)
    root.after(30,setup)
    root.after(7000,lambda:fail(AssertionError('Celkový limit GUI testu')))
    return original_loop(root,*a,**kw)

with tempfile.TemporaryDirectory() as folder:
    work=Path(folder)
    for file in (ROOT/'courses/tkinter-api/lessons'/IDS[args.lesson]/'files').iterdir():
        if file.is_file():shutil.copy2(file,work/file.name)
    os.chdir(work);sys.path.insert(0,str(work))
    import kurzy
    original_client=kurzy.nacti_kurz
    def client(address,currency,**options):
        global inflight,maximum
        with lock:
            if flags['fail_next']:
                address=address.replace('/pomalu','/chyba');flags['fail_next']=False
            request_log.append({'thread':threading.get_ident(),'url':address,'currency':currency})
            inflight+=1;maximum=max(maximum,inflight)
        try:return original_client(address,currency,**options)
        finally:
            with lock:inflight-=1
    kurzy.nacti_kurz=client
    tk.Tk.mainloop=mainloop
    try:
        runpy.run_path(str(ROOT/'courses/tkinter-api/lessons'/IDS[args.lesson]/'example.py'),run_name='__main__')
        assert len(entered)==1 and not failures,failures
        print(f'OK: skutečné Tk {tk.TkVersion}, lekce {args.lesson}, místní HTTP, odezva, chyba a nový pokus')
    finally:tk.Tk.mainloop=original_loop
