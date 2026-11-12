"""Nativní Tk test: DISPLAY=:97 python tests/native_bmi_tracker.py [--shots DIR].

Používá čtyři nové GUI procesy, uložené spouštěče, skutečný CSV export a backup.
"""
from contextlib import closing
import csv
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent.parent
IDS=['19-projekt-bmi-tracker','20-export-zaloha-a-testy-trackeru']
shots=Path(sys.argv[sys.argv.index('--shots')+1]).resolve() if '--shots' in sys.argv else None
if shots:shots.mkdir(parents=True,exist_ok=True)
if not os.environ.get('DISPLAY'):raise SystemExit('Pro skutečný Tk nastavte DISPLAY dostupné grafické plochy.')
DRIVER=r'''
import runpy,sys,traceback,sqlite3
from pathlib import Path
import tkinter as tk
entry,scenario,shot,stage,*args=sys.argv[1:]
sys.argv=[entry,*args];sys.path.insert(0,str(Path(entry).parent))
if stage=='19':
    from reseni import Aplikace
else:
    from aplikace import Aplikace
init=Aplikace.__init__
def attach(self,root,model):
    init(self,root,model);root._app=self
Aplikace.__init__=attach
original=tk.Tk;errors=[]
def walk(root):
    for w in root.winfo_children():yield w;yield from walk(w)
def named(root,name):return next(w for w in walk(root) if w.winfo_name()==name)
def fill(root,name,text):
    w=named(root,name);w.delete(0,'end');w.insert(0,text)
def click(root,text):
    next(w for w in walk(root) if w.winfo_class()=='TButton' and w.cget('text')==text).invoke();root.update()
def items(root):return named(root,'mereni').get(0,'end')
class ControlledTk(original):
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw);self.after(200,self.exercise)
    def report_callback_exception(self,typ,value,tb):errors.append(''.join(traceback.format_exception(typ,value,tb)))
    def exercise(self):
        try:
            if scenario=='create':
                assert items(self)==()
                fill(self,'den','2026-02-29');fill(self,'hmotnost','72,5');fill(self,'poznamka','Rozepsáno')
                click(self,'Uložit měření')
                assert items(self)==() and named(self,'hmotnost').get()=='72,5'
                fill(self,'den','2026-04-03');click(self,'Uložit měření')
                assert named(self,'hmotnost').get()==''
                for den,h,v,note in [('2026-04-01','81','180','Žofie; "text"'),('2026-04-05','82','200','  mezery  ')]:
                    for name,text in [('den',den),('hmotnost',h),('vyska',v),('poznamka',note)]:fill(self,name,text)
                    click(self,'Uložit měření')
                assert len(items(self))==3
                fill(self,'od','2026-04-03');fill(self,'do','2026-04-03');click(self,'Použít období')
                assert items(self)==('1: 2026-04-03 | 72.5 kg / 180 cm | BMI 22.38',)
                fill(self,'od','2026-05-01');click(self,'Použít období')
                assert len(items(self))==1
                click(self,'Všechna měření');assert len(items(self))==3
                self._app.model.con.execute('PRAGMA query_only=ON')
                fill(self,'den','2026-04-06');fill(self,'hmotnost','71,2');fill(self,'poznamka','Neztratit při chybě')
                click(self,'Uložit měření')
                assert named(self,'stav').cget('text')=='Měření se nepodařilo uložit do databáze.'
                assert named(self,'hmotnost').get()=='71,2' and named(self,'poznamka').get()=='Neztratit při chybě'
                self._app.model.con.execute('PRAGMA query_only=OFF')
            else:
                assert len(items(self))==3,items(self)
                assert items(self)[0].startswith('2: 2026-04-01')
            assert not errors,errors
            for geometry in ['840x700','650x600']:
                self.geometry(geometry);self.update()
                for w in walk(self):
                    if w.winfo_ismapped():
                        assert w.winfo_x()+w.winfo_width()<=w.master.winfo_width()+2,(w,'šířka')
                        assert w.winfo_y()+w.winfo_height()<=w.master.winfo_height()+2,(w,'výška')
                if shot:
                    from PIL import ImageGrab
                    x,y=self.winfo_rootx(),self.winfo_rooty()
                    ImageGrab.grab(bbox=(x,y,x+self.winfo_width(),y+self.winfo_height())).save(shot.replace('.png','-'+geometry+'.png'))
        except BaseException:errors.append(traceback.format_exc())
        finally:self.destroy()
tk.Tk=ControlledTk
runpy.run_path(entry,run_name='__main__')
if errors:raise AssertionError('\n'.join(errors))
'''
python=os.environ.get('DILNA_TEST_PYTHON') or sys.executable
with tempfile.TemporaryDirectory() as temp:
    works=[]
    for lid in IDS:
        source=ROOT/'courses/databaze/lessons'/lid;work=Path(temp)/lid
        shutil.copytree(source/'files',work);(work/'reseni.py').write_bytes((source/'solution.py').read_bytes());works.append(work)
    db=works[0]/'bmi.sqlite3'
    def gui(index,scenario,path):
        entry=works[index]/'spust_bmi.py';shot=str(shots/f'bmi-{19+index}-{scenario}.png') if shots else ''
        run=subprocess.run([python,'-X','utf8','-c',DRIVER,str(entry),scenario,shot,str(19+index),'--db',str(path)],cwd=temp,capture_output=True,text=True,timeout=20)
        assert run.returncode==0,run.stdout+run.stderr
    gui(0,'create',db);gui(0,'reopen',db);gui(1,'reopen',db)
    with closing(sqlite3.connect(db,autocommit=True)) as con:
        assert con.execute('SELECT COUNT(*) FROM mereni').fetchone()==(3,)
        assert con.execute('SELECT hmotnost,poznamka FROM mereni WHERE id=1').fetchone()==(72.5,'Rozepsáno')
    export=works[1]/'vystup.csv';backup=works[1]/'kopie.sqlite3'
    for args in [('export',str(export)),('zaloha',str(backup))]:
        run=subprocess.run([python,str(works[1]/'spust_bmi.py'),'--db',str(db),*args],cwd=temp,capture_output=True,text=True,timeout=10)
        assert run.returncode==0,run.stdout+run.stderr
    with export.open(encoding='utf-8',newline='') as f:rows=list(csv.reader(f,delimiter=';'))
    assert len(rows)==4 and rows[1][-1]=='Žofie; "text"'
    gui(1,'backup',backup)
    print('OK: čtyři skutečné Tk procesy 19/20, 840x700/650x600, validace/čárka/období/read-only chyba, vlastní data, CSV, backup a znovuotevření')
