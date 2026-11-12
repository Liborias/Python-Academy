"""Půjčovna 26–30: hranice zadání, účinnost testů a skutečné předání mezi procesy."""
import ast
import csv
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check
from server.content import lesson_view,solution_view
BASE=ROOT/'courses/databaze/lessons'
IDS=['26-luhn-a-inventarni-cislice','27-volitelne-qr-stitky','28-vlastni-testy-pujcovny','29-cesty-zaloha-a-predani','30-moje-pujcovna-a-zaverecne-overeni']

class PredaniPujcovnyTest(unittest.TestCase):
    def source(self,i):return (BASE/IDS[i]/'solution.py').read_text()
    def check(self,i,code,expected):
        with tempfile.TemporaryDirectory() as temp:r=run_check(BASE/IDS[i],code,ROOT/'lib',Path(temp))
        self.assertNotIn('error',r,r);self.assertEqual(r['ok'],expected,r)
    def variants(self,i,changes,old,new):
        source=self.source(i)
        for a,b in changes:
            self.assertIn(a,source)
            with self.subTest(stage=i,change=a):self.check(i,source.replace(a,b),False)
        self.assertIn(old,source);self.check(i,source.replace(old,new),True)

    def test_references_and_starters(self):
        for i,lid in enumerate(IDS):
            self.check(i,self.source(i),True);self.check(i,(BASE/lid/'exercise.py').read_text(),False)

    def test_luhn_parity_zeros_ascii_and_limited_detection(self):
        self.variants(0,[('index % 2 == 0','index % 2 == 1'),('str((-soucet) % 10)','str(soucet % 10)'),
                         ('or not all(',"or kod.startswith('0') or not all("),("all('0'<=c<='9' for c in kod)",'kod.isdigit()')],
                      'soucet','mezisoucet')

    def test_qr_optional_backend_exact_bytes_profile_and_atomic_save(self):
        self.variants(1,[('over_qr_text(text)','over_qr_text(text.strip())'),('box_size=6','box_size=1'),
                         ('border=4','border=0'),("format='PNG'","format='JPEG'"),
                         ('if knihovna is None:\n        return None','if knihovna is None:\n        cil.write_bytes(b\"\")\n        return None')],
                      'knihovna.QRCode(error_correction=', 'knihovna.QRCode(version=None, error_correction=')

    def test_own_suite_rejects_vacuous_assertions_and_wrong_class(self):
        self.variants(2,[('return unittest.defaultTestLoader.loadTestsFromTestCase(TestPujcovny)','return unittest.TestSuite()'),
                         ('self.assertEqual(self.model.prehled()[0][2],1)','self.assertEqual(1,1)'),
                         ('self.model = Pujcovna(self.cesta)','from model import Pujcovna as PevnyModel\n            self.model = PevnyModel(self.cesta)')],
                      'TestPujcovny','OvereniModelu')

    def test_paths_are_pure_and_backup_is_independent(self):
        self.variants(3,[('Path(soubor).resolve().parent','Path.cwd()'),
                         ('model.con.backup(target)','pass'),('bezpecny_cil(cesta,model.cesta)','bezpecny_cil(cesta,None)')],
                      'databaze','cesta_db')

    def test_final_left_join_active_counts_sparse_ids_and_csv(self):
        self.variants(4,[('LEFT JOIN','JOIN'),('COUNT(v.id)','COUNT(*)'),(' AND v.vraceno=0',''),
                         ('kusy+pocet','kusy'),('ORDER BY p.id','ORDER BY p.id DESC'),
                         ('delimiter=\';\'','delimiter=\',\''),('zapis.writerows(karty)',"zapis.writerows([{**k,'dostupne':999} for k in karty])")],
                      'self.con.execute(','self.con.cursor().execute(')

    def test_scope_prior_definitions_and_solutions(self):
        course=json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(next(m for m in course['modules'] if m['id']=='m06')['lessons'],IDS)
        def defs(code):return [ast.dump(n) for n in ast.parse(code).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
        for i,lid in enumerate(IDS):
            d=BASE/lid;v=lesson_view(ROOT/'courses','databaze',lid)
            self.assertEqual((v['kind'],len(v['examples']),len(v['tasks']),len(v['quiz'])),('console',2 if i==0 else 0,0,3))
            self.assertEqual(solution_view(ROOT/'courses','databaze',lid)['code'],self.source(i))
            for name,prior in [('luhn.py',0),('qr_export.py',1),('sada.py',2),('predani.py',3)]:
                p=d/'files'/name
                if p.exists():self.assertEqual(defs(p.read_text()),defs(self.source(prior)))
            if i>=2:
                self.assertEqual(defs((d/'files/evidence.py').read_text()),defs((BASE/'10-projekt-klubovni-evidence/solution.py').read_text()))
        self.assertTrue(json.loads((BASE/IDS[1]/'lesson.json').read_text())['preview_images'])
        self.assertTrue(json.loads((BASE/IDS[4]/'lesson.json').read_text())['download_files'])

    def test_console_examples_and_markdown_snippets(self):
        count=0
        for i,lid in enumerate(IDS):
            d=BASE/lid;sources=[self.source(i),*re.findall(r'```python\n(.*?)```',(d/'lesson.md').read_text(),re.S)]
            if (d/'examples.json').exists():sources += [v['code'] for v in json.loads((d/'examples.json').read_text())]
            for source in sources:
                with tempfile.TemporaryDirectory() as temp:
                    w=Path(temp);shutil.copytree(d/'files',w,dirs_exist_ok=True);(w/'reseni.py').write_text(source,encoding='utf-8')
                    r=subprocess.run([sys.executable,'-X','utf8','reseni.py'],cwd=w,capture_output=True,text=True,timeout=15)
                    self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertEqual(list(w.glob('*.sqlite3')),[]);count+=1
        self.assertEqual(count,12)

    def test_saved_cli_reopen_return_backup_csv_and_supplied_tests(self):
        with tempfile.TemporaryDirectory() as temp:
            for i,n in [(3,6),(4,8)]:
                work=Path(temp)/f'Moje půjčovna {i}';shutil.copytree(BASE/IDS[i]/'files',work);(work/'reseni.py').write_text(self.source(i))
                def run(entry,*args,expected=0):
                    r=subprocess.run([sys.executable,'-X','utf8',str(work/entry),*map(str,args)],cwd=temp,capture_output=True,text=True,timeout=15)
                    self.assertEqual(r.returncode,expected,r.stdout+r.stderr);return r.stdout+r.stderr
                def cli(*args,**kw):return run('spust_pujcovnu.py',*args,**kw)
                cli('--help');self.assertFalse((work/'pujcovna.sqlite3').exists())
                self.assertIn(f'Ran {n} tests',run('overeni.py'));self.assertFalse((work/'pujcovna.sqlite3').exists())
                self.assertIn('kód: 18',cli('pridat',"Karty; O'Neil",2))
                self.assertIn('Výpůjčka ID: 1',cli('pujcit','18','Žofie'))
                cli('pujcit','19','Žofie',expected=2)
                self.assertIn('Žofie',cli('vypujcky'));backup=work/'kopie.sqlite3';cli('zaloha',backup)
                self.assertIn('True',cli('vratit',1));self.assertIn('False',cli('vratit',1))
                self.assertNotIn('Žofie',cli('vypujcky'));self.assertIn('Žofie',cli('--db',backup,'vypujcky'))
                cli('zaloha',work/'pujcovna.sqlite3',expected=2)
                if i==4:
                    path=work/'štítky.csv';self.assertIn('Exportováno: 1',cli('export',path))
                    with path.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
                    self.assertEqual(rows[0],{'id':'1','nazev':"Karty; O'Neil",'kod':'18','dostupne':'2','vypujceno':'0','celkem':'2'})
                    cli('export',work/'pujcovna.sqlite3',expected=2);cli('qr',999,work/'x.png',expected=2)
                self.assertEqual(list(work.glob('.bmi-*')),[])

if __name__=='__main__':unittest.main()
