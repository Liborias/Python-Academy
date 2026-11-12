"""Volitelný PostgreSQL: offline kontrakt, vlastnictví, pool a uložený spouštěč."""
import ast
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock,patch

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check
from server.content import lesson_view,solution_view
BASE=ROOT/'courses/databaze/lessons'
IDS=['31-postgresql-pripojeni-a-parametry','32-pool-a-sprava-spojeni']

class PostgreSQLTest(unittest.TestCase):
    def source(self,i):return (BASE/IDS[i]/'solution.py').read_text()
    def check(self,i,source,ok):
        with tempfile.TemporaryDirectory() as t:r=run_check(BASE/IDS[i],source,ROOT/'lib',Path(t))
        self.assertNotIn('error',r,r);self.assertEqual(r['ok'],ok,r)
    def test_references_and_starters(self):
        for i,lid in enumerate(IDS):
            self.check(i,self.source(i),True);self.check(i,(BASE/lid/'exercise.py').read_text(),False)

    def test_parameters_identity_filter_and_connection_owner(self):
        s=self.source(0)
        for a,b in [('VALUES(%s,%s)','VALUES(?,?)'),('return cur.fetchone()[0]','return 999'),
                    ('kusy >= %s','kusy > %s'),('ORDER BY id','ORDER BY nazev'),('SELECT id,nazev,kusy','SELECT kusy,nazev,id'),('RETURNING id','RETURNING id+1'),
                    ('nazev_pomucky(nazev)', 'nazev_pomucky(nazev.replace("\'", ""))'),('return cur.fetchall()','return []')]:
            self.assertIn(a,s);self.check(0,s.replace(a,b),False)
        good=s.replace('with con.cursor() as cur:\n            cur.execute(', 'with con.execute(').replace('(nazev,kusy))','(nazev,kusy)) as cur:').replace('(minimum,))','(minimum,)) as cur:')
        self.check(0,good,True)
        swapped=s.replace('akademie_pomucky(nazev,kusy)','akademie_pomucky(kusy,nazev)').replace('(nazev,kusy))','(kusy,nazev))')
        self.check(0,swapped,True)

    def test_pool_whole_batch_validation_rollback_and_release(self):
        s=self.source(1)
        for a,b in [('if not pomucky:','if False:'),('timeout=3','timeout=None'),('return prehled_pg(con,minimum)','return []'),
                    ('pomucky = priprav_davku(pomucky)','pomucky = pomucky'),
                    ('with con.transaction():\n            return [pridej_pg(con,nazev,kusy) for nazev,kusy in pomucky]','return [pridej_pg(con,nazev,kusy) for nazev,kusy in pomucky]')]:
            self.assertIn(a,s);self.check(1,s.replace(a,b),False)
        self.check(1,s.replace('pomucky = priprav_davku(pomucky)','pomucky = list(priprav_davku(pomucky))'),True)

    def test_driver_configuration_lazy_open_wait_and_cleanup(self):
        ns=runpy.run_path(str(BASE/IDS[0]/'files/pg_podpora.py'),run_name='probe')
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaises(ValueError):ns['pripoj']()
        env={'PGHOST':'127.0.0.1','PGPORT':'5432','PGDATABASE':'akademie','PGUSER':'akademie'}
        connection=Mock();connect=Mock(return_value=connection);pool=Mock();factory=Mock(return_value=pool)
        with patch.dict(os.environ,env,clear=True),patch.dict(sys.modules,{'psycopg':SimpleNamespace(connect=connect),'psycopg_pool':SimpleNamespace(ConnectionPool=factory)}):
            self.assertIs(ns['pripoj']('Fiktivní heslo'),connection)
            connect.assert_called_once_with('',autocommit=True,connect_timeout=5,application_name='python-akademie',password='Fiktivní heslo')
            self.assertIs(ns['priprav_pool'](),pool)
            self.assertEqual(factory.call_args.kwargs,{'min_size':1,'max_size':3,'timeout':3,'kwargs':{'autocommit':True,'connect_timeout':5,'application_name':'python-akademie'},'open':False})
            pool.open.assert_called_once_with(wait=True,timeout=8);pool.close.assert_not_called()
            pool.open.side_effect=TimeoutError('Řízený start')
            with self.assertRaises(TimeoutError):ns['priprav_pool']()
            pool.close.assert_called_once()
        with patch.dict(os.environ,env,clear=True),patch.dict(sys.modules,{'psycopg':None,'psycopg_pool':None}):
            with self.assertRaises(RuntimeError):ns['pripoj']()
            with self.assertRaises(RuntimeError):ns['priprav_pool']()

    def test_scope_and_exact_prior_model(self):
        course=json.loads((BASE.parent/'course.json').read_text());self.assertEqual(course['modules'][-1]['lessons'],IDS)
        def defs(source):return [ast.dump(n) for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)]
        self.assertEqual(defs((BASE/IDS[1]/'files/pg_model.py').read_text()),defs(self.source(0)))
        for i,lid in enumerate(IDS):
            v=lesson_view(ROOT/'courses','databaze',lid)
            self.assertEqual((v['kind'],len(v['examples']),len(v['tasks']),len(v['quiz'])),('console',2,0,3))
            self.assertEqual(solution_view(ROOT/'courses','databaze',lid)['code'],self.source(i))

    def test_offline_examples_and_explanatory_snippets(self):
        count=0
        for i,lid in enumerate(IDS):
            d=BASE/lid;sources=[self.source(i),*[v['code'] for v in json.loads((d/'examples.json').read_text())],*re.findall(r'```python\n(.*?)```',(d/'lesson.md').read_text(),re.S)]
            for code in sources:
                with tempfile.TemporaryDirectory() as t:
                    w=Path(t);shutil.copytree(d/'files',w,dirs_exist_ok=True);(w/'reseni.py').write_text(code)
                    r=subprocess.run([sys.executable,'-S','-X','utf8','reseni.py'],cwd=w,capture_output=True,text=True,timeout=10)
                    self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertEqual(list(w.glob('*.sqlite3')),[]);count+=1
        self.assertEqual(count,8)

    def test_saved_cli_help_simulation_missing_settings_and_driver(self):
        for i,lid in enumerate(IDS):
            with tempfile.TemporaryDirectory() as t:
                w=Path(t)/'Můj PostgreSQL';shutil.copytree(BASE/lid/'files',w);(w/'reseni.py').write_text(self.source(i))
                env={k:v for k,v in os.environ.items() if not k.startswith('PG')};env.update({'PYTHONUTF8':'1'})
                def cli(*args,expected=0):
                    r=subprocess.run([sys.executable,'-S','-X','utf8',str(w/'spust_postgres.py'),*args],cwd=t,env=env,capture_output=True,text=True,timeout=10)
                    self.assertEqual(r.returncode,expected,r.stdout+r.stderr);return r.stdout+r.stderr
                self.assertIn('--pripojit',cli('--help'));self.assertIn('VÝUKOVÁ SIMULACE',cli())
                cli('--heslo',expected=2);cli('init',expected=2)
                self.assertIn('PGHOST',cli('--pripojit','init',expected=2))
                env.update({'PGHOST':'127.0.0.1','PGPORT':'1','PGDATABASE':'fiktivni','PGUSER':'fiktivni'})
                self.assertIn('VÝUKOVÁ SIMULACE',cli())
                self.assertIn('Doinstalujte',cli('--pripojit','init',expected=2));self.assertEqual(list(w.glob('*.sqlite3')),[])
                if i==1:
                    r=subprocess.run([sys.executable,'-S',str(w/'pokus_davky.py')],cwd=t,env=env,capture_output=True,text=True,timeout=10)
                    self.assertEqual(r.returncode,0,r.stderr);self.assertIn('VÝUKOVÁ SIMULACE',r.stdout)

    def test_import_does_not_require_driver_or_open_a_connection(self):
        for i,lid in enumerate(IDS):
            with tempfile.TemporaryDirectory() as t:
                w=Path(t);shutil.copytree(BASE/lid/'files',w,dirs_exist_ok=True);(w/'reseni.py').write_text(self.source(i))
                r=subprocess.run([sys.executable,'-S','-c','import reseni, pg_podpora; print("Pouze definice")'],cwd=w,capture_output=True,text=True,timeout=10)
                self.assertEqual((r.returncode,r.stdout.strip()),(0,'Pouze definice'),r.stderr)

if __name__=='__main__':unittest.main()
