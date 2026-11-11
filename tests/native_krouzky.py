"""Ruční integrační test se skutečným Tk: DISPLAY=:97 python tests/native_krouzky.py.

Vyžaduje dostupnou grafickou plochu; nespouští se v unittest discover.
Samostatné procesy ovládají uložené spouštěče, ověřují DB a nové otevření.
"""
import os
from contextlib import closing
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent.parent
IDS=['12-formular-a-pridani-krouzku','13-upravy-a-mazani-krouzku','14-prihlasky-a-kapacita','15-dokonceni-a-testy-evidence']
shots=Path(sys.argv[sys.argv.index('--shots')+1]).resolve() if '--shots' in sys.argv else None
if shots:shots.mkdir(parents=True,exist_ok=True)
if not os.environ.get('DISPLAY'):
    raise SystemExit('Nastavte DISPLAY na dostupnou grafickou plochu pro skutečný Tkinter.')
DRIVER=r'''
from pathlib import Path
import runpy,sys,traceback
import tkinter as tk
entry,scenario,shot,*db_args=sys.argv[1:]
sys.argv=[entry,*db_args]
sys.path.insert(0,str(Path(entry).parent))
original=tk.Tk
errors=[]
def walk(root):
    for w in root.winfo_children():
        yield w
        yield from walk(w)
def named(root,name):
    return next(w for w in walk(root) if w.winfo_name()==name)
def fill(root,name,value):
    w=named(root,name);w.delete(0,'end');w.insert(0,value)
def click(root,text):
    next(w for w in walk(root) if w.winfo_class()=='TButton' and w.cget('text')==text).invoke()
    root.update()
def choose(root,name,index):
    w=named(root,name);w.selection_clear(0,'end');w.selection_set(index)
    w.event_generate('<<ListboxSelect>>');root.update()
def add(root,name,cap):
    fill(root,'nazev',name);fill(root,'kapacita',cap);click(root,'Přidat kroužek')
def items(root,name):return named(root,name).get(0,'end')
class ControlledTk(original):
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw)
        self.after(200,self.exercise)
    def report_callback_exception(self,typ,value,tb):
        errors.append(''.join(traceback.format_exception(typ,value,tb)))
    def exercise(self):
        try:
            self.update()
            if scenario=='reopen':
                assert len(items(self,'krouzky'))>=1,items(self,'krouzky')
            else:
                assert items(self,'krouzky')==()
                add(self,'  Robotika  ','2');add(self,'Šachy','3')
                add(self,'Rozepsáno','1.5')
                assert named(self,'nazev').get()=='Rozepsáno'
                assert len(items(self,'krouzky'))==2
                if scenario=='12':
                    add(self,"  Karty O'Neil  ",'1')
                    assert len(items(self,'krouzky'))==3
                elif scenario=='13':
                    choose(self,'krouzky',0);click(self,'Smazat kroužek')
                    choose(self,'krouzky',0)
                    assert named(self,'nazev').get()=='Šachy'
                    fill(self,'nazev','Nové šachy');fill(self,'kapacita','4');click(self,'Uložit změny')
                    add(self,'Další','2');choose(self,'krouzky',1);click(self,'Smazat kroužek')
                    assert items(self,'krouzky')==('2: Nové šachy (kapacita 4)',)
                else:
                    choose(self,'krouzky',0)
                    for name in ['  Žofie  ','Ada']:
                        fill(self,'clen',name);click(self,'Přihlásit člena')
                    fill(self,'clen','Navíc');click(self,'Přihlásit člena')
                    assert named(self,'stav').cget('text')=='Kroužek je plný.'
                    assert named(self,'clen').get()=='Navíc'
                    fill(self,'kapacita','1');click(self,'Uložit změny')
                    assert named(self,'stav').cget('text')=='Kapacita nesmí být menší než počet přihlášek.'
                    click(self,'Smazat kroužek')
                    assert len(items(self,'krouzky'))==2
                    choose(self,'prihlasky',0);click(self,'Odhlásit člena')
                    fill(self,'clen',"  O'Neil  ");click(self,'Přihlásit člena')
                    choose(self,'prihlasky',1);click(self,'Odhlásit člena')
                    assert items(self,'prihlasky')==('2: Ada',)
                    assert named(self,'obsazenost').cget('text')=='Obsazeno 1 / 2'
            assert not errors,errors
            self.update_idletasks()
            for w in walk(self):
                if w.winfo_ismapped():
                    assert w.winfo_x()>=0 and w.winfo_y()>=0
                    assert w.winfo_x()+w.winfo_width()<=w.master.winfo_width()+2,(w,w.winfo_width(),w.master.winfo_width())
            self.geometry('680x600')
            self.update()
            for w in walk(self):
                if w.winfo_ismapped():
                    assert w.winfo_x()+w.winfo_width() <= w.master.winfo_width()+2
                    assert w.winfo_y()+w.winfo_height() <= w.master.winfo_height()+2,(w,w.winfo_height(),w.master.winfo_height())
            if shot:
                from PIL import ImageGrab
                x,y=self.winfo_rootx(),self.winfo_rooty()
                ImageGrab.grab(bbox=(x,y,x+self.winfo_width(),y+self.winfo_height())).save(shot)
        except BaseException:
            errors.append(traceback.format_exc())
        finally:
            self.destroy()
tk.Tk=ControlledTk
runpy.run_path(entry,run_name='__main__')
if errors:raise AssertionError('\n'.join(errors))
print('OK native',scenario)
'''
python=os.environ.get('DILNA_TEST_PYTHON') or sys.executable
with tempfile.TemporaryDirectory() as temp:
    for index,lid in enumerate(IDS):
        source=ROOT/'courses/databaze/lessons'/lid
        work=Path(temp)/lid;shutil.copytree(source/'files',work)
        (work/'reseni.py').write_bytes((source/'solution.py').read_bytes())
        entry=str(work/'spust_krouzky.py')
        for scenario in [str(12+index),'reopen']:
            shot=str(shots/f'native-{12+index}-{scenario}.png') if shots else ''
            run=subprocess.run([python,'-X','utf8','-c',DRIVER,entry,scenario,shot],cwd=temp,capture_output=True,text=True,timeout=20)
            assert run.returncode==0,(lid,scenario,run.stdout+run.stderr)
        with closing(sqlite3.connect(work/'krouzky.sqlite3',autocommit=True)) as con:
            rows=con.execute('SELECT id,nazev,kapacita FROM krouzky ORDER BY id').fetchall()
            if index==0:assert rows==[(1,'Robotika',2),(2,'Šachy',3),(3,"Karty O'Neil",1)],rows
            elif index==1:assert rows==[(2,'Nové šachy',4)],rows
            else:
                assert rows==[(1,'Robotika',2),(2,'Šachy',3)],rows
                assert con.execute('SELECT id,krouzek_id,clen FROM prihlasky').fetchall()==[(2,1,'Ada')]
        if index == 3:
            predchozi = Path(temp)/IDS[2]/'krouzky.sqlite3'
            run = subprocess.run([python,'-X','utf8','-c',DRIVER,entry,'reopen','', '--db',str(predchozi)],
                                 cwd=temp,capture_output=True,text=True,timeout=20)
            assert run.returncode == 0, run.stdout+run.stderr
        print('OK: uložený spouštěč',lid,'dva skutečné Tk procesy a trvalý SQLite soubor')
