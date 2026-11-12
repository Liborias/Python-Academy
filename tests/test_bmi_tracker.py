"""BMI: jednotky/hranice, data/období, GUI a nezávislý export/backup."""
import ast
import csv
import json
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check
from server.content import lesson_view,solution_view
BASE=ROOT/'courses/databaze/lessons'
IDS=['16-bmi-vypocet-a-jednotky','17-mereni-a-datum-v-sqlite','18-obdobi-a-souhrny-mereni','19-projekt-bmi-tracker','20-export-zaloha-a-testy-trackeru']


class BmiTrackerTest(unittest.TestCase):
    def source(self,i):return (BASE/IDS[i]/'solution.py').read_text()
    def check(self,i,code,expected):
        with tempfile.TemporaryDirectory() as temp:r=run_check(BASE/IDS[i],code,ROOT/'lib',Path(temp))
        self.assertNotIn('error',r,r);self.assertEqual(r['ok'],expected,r)
    def variants(self,i,changes):
        source=self.source(i)
        for before,after in changes:
            self.assertIn(before,source)
            with self.subTest(stage=i,change=before):self.check(i,source.replace(before,after),False)
        if i==0:good=source.replace('(hmotnost_kg / vyska_m) / vyska_m','hmotnost_kg / (vyska_m * vyska_m)')
        elif i==3:good=source.replace('ident','klic')
        else:good=source.replace('self.con.execute(','self.con.cursor().execute(') if i==1 else source.replace('radky','vybrane_radky')
        self.assertNotEqual(good,source);self.check(i,good,True)

    def test_references_accept_starters_reject(self):
        for i,lid in enumerate(IDS):
            self.check(i,self.source(i),True)
            self.check(i,(BASE/lid/'exercise.py').read_text(),False)

    def test_units_finiteness_bool_and_unrounded_bands(self):
        self.variants(0,[('/ 100','/ 1'),('return hodnota','return round(hodnota, 2)'),
                         ('hodnota < 25','hodnota <= 25'),('hodnota < 18.5','round(hodnota, 2) < 18.5'),
                         ('hmotnost_kg = kladne_cislo(hmotnost_kg)','hmotnost_kg = float(hmotnost_kg)')])

    def test_model_own_transaction_date_order_and_note(self):
        self.variants(1,[('hodnoty = over_mereni(den, hmotnost, vyska_cm, poznamka)','hodnoty = (den, hmotnost, vyska_cm, poznamka)'),
                         ("with self.con:\n            return self.con.execute('INSERT", "if True:\n            return self.con.execute('INSERT"),
                         ('ORDER BY den,id','ORDER BY id'),('self.con.close()','pass')])

    def test_inclusive_period_empty_average_and_chronology(self):
        self.variants(2,[('from statistics import mean', 'from statistics import fmean as mean'),('bmi(h, v)','round(bmi(h, v), 2)'),('den >= ?','den > ?'),('den <= ?','den < ?'),('ORDER BY den,id','ORDER BY id'),
                         ('if od is not None and do is not None and od > do:','if False:'),
                         ('mean(r[4] for r in radky)','bmi(mean(r[2] for r in radky), mean(r[3] for r in radky))'),
                         ("'prumer_bmi': mean(r[4] for r in radky) if radky else None", "'prumer_bmi': mean(r[4] for r in radky) if radky else 0")])

    def test_form_validation_locale_filter_and_draft(self):
        self.variants(3,[("self.w['hmotnost'].delete(0, tk.END)",'pass'),
                         ('cti_cislo(self.w[\'hmotnost\'].get())','float(self.w[\'hmotnost\'].get())'),
                         ('self.model.prehled(od, do)','self.model.prehled()'),
                         ("self.obnov(od, do)", "self.w['mereni'].delete(0, tk.END)\n            self.obnov(od, do)"),
                         ("self.w['od'].delete(0, tk.END)",'pass')])

    def test_csv_quoting_headers_filter_and_backup_api(self):
        self.variants(4,[('zapis.writerows(radky)', 'zapis.writerows([(*r[:4], round(r[4],2), r[5]) for r in radky])'),("delimiter=';'", "delimiter=','"),('self.prehled(od, do)','self.prehled()'),
                         ('zapis.writerows(radky)', 'zapis.writerows([r[:-1] + (r[-1].strip(),) for r in radky])'),
                         ('return len(radky)','return len(radky) + 1'),('self.con.backup(target)','pass'),
                         ('bezpecny_cil(cesta, self.cesta)','bezpecny_cil(cesta)')])

    def test_scope_helpers_and_reference_identity(self):
        course=json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(next(m for m in course['modules'] if m['id']=='m04')['lessons'],IDS)
        for i,lid in enumerate(IDS):
            view=lesson_view(ROOT/'courses','databaze',lid)
            self.assertEqual(view['kind'],'gui' if i==3 else 'console')
            self.assertEqual(len(view['examples']),2 if i==0 else 0)
            self.assertEqual(view['tasks'],[]);self.assertEqual(len(view['quiz']),3)
            self.assertEqual(solution_view(ROOT/'courses','databaze',lid)['code'],self.source(i))
            for name,prior in [('vypocet.py',0),('model.py',1),('prehledy.py',2),('aplikace.py',3)]:
                helper=BASE/lid/'files'/name
                if helper.exists():
                    expected=[ast.dump(n) for n in ast.parse(self.source(prior)).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))]
                    got=[ast.dump(n) for n in ast.parse(helper.read_text()).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))]
                    self.assertEqual(got,expected)

    def test_all_console_examples_and_markdown_snippets_standalone(self):
        count=0
        for i,lid in enumerate(IDS):
            d=BASE/lid
            sources=re.findall(r'```python\n(.*?)```',(d/'lesson.md').read_text(),re.S)
            if i!=3:sources.append(self.source(i))
            if i==0:sources.extend(e['code'] for e in json.loads((d/'examples.json').read_text()))
            for code in sources:
                with tempfile.TemporaryDirectory() as temp:
                    work=Path(temp);shutil.copytree(d/'files',work,dirs_exist_ok=True)
                    (work/'reseni.py').write_text(code,encoding='utf-8')
                    run=subprocess.run([sys.executable,'-X','utf8','reseni.py'],cwd=work,capture_output=True,text=True,timeout=10)
                    self.assertEqual(run.returncode,0,run.stdout+run.stderr)
                    self.assertEqual(list(work.glob('*.sqlite3')),[])
                    self.assertEqual(list(work.glob('*.csv')),[])
                    count+=1
        self.assertEqual(count,11)

    def test_exported_cli_tests_and_help_without_graphical_imports(self):
        d=BASE/IDS[4]
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp)/'BMI s mezerou';shutil.copytree(d/'files',work)
            (work/'reseni.py').write_text(self.source(4),encoding='utf-8')
            entry=work/'spust_bmi.py'
            driver="""import sys,runpy
from pathlib import Path
entry=sys.argv[1];sys.path.insert(0,str(Path(entry).parent));sys.argv=sys.argv[1:]
class BezTk:
    def find_spec(self,fullname,*args):
        if fullname=='tkinter' or fullname.startswith('tkinter.'):
            raise AssertionError('Tato větev nesmí importovat Tkinter')
sys.meta_path.insert(0,BezTk())
runpy.run_path(entry,run_name='__main__')
"""
            def cli(*args,expected=0):
                run=subprocess.run([sys.executable,'-X','utf8','-c',driver,str(entry),*args],cwd=temp,capture_output=True,text=True,timeout=15)
                self.assertEqual(run.returncode,expected,run.stdout+run.stderr);return run.stdout
            cli('--help');self.assertFalse((work/'bmi.sqlite3').exists())
            setup="from reseni import Tracker\nm=Tracker('bmi.sqlite3')\nm.pridej('2026-04-01',81,180,'Žofie; test')\nm.close()"
            run=subprocess.run([sys.executable,'-X','utf8','-c',setup],cwd=work,capture_output=True,text=True,timeout=10)
            self.assertEqual(run.returncode,0,run.stderr)
            export=work/'export.csv';backup=work/'kopie.sqlite3'
            self.assertIn('Exportováno řádků: 1',cli('export',str(export)))
            self.assertIn('Záloha:',cli('zaloha',str(backup)))
            self.assertEqual(export.read_text(encoding='utf-8').count('Žofie; test'),1)
            self.assertTrue(backup.read_bytes().startswith(b'SQLite format 3\x00'))
            cli('export',str(export),'--od','2026-05-01','--do','2026-04-01',expected=2)
            cli('zaloha',str(work/'bmi.sqlite3'),expected=2)
            run=subprocess.run([sys.executable,'-X','utf8','overeni.py'],cwd=work,capture_output=True,text=True,timeout=15)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr);self.assertIn('Ran 3 tests',run.stderr)
            self.assertEqual(list(work.glob('.bmi-*')),[])


if __name__=='__main__':unittest.main()
