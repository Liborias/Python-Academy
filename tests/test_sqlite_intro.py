"""SQLite úvod: chování SQL, alternativy, soubory, rollback a výukové ukázky."""
import ast
from contextlib import closing
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
IDS=['01-sqlite-spojeni-a-soubor','02-tabulky-a-omezeni','03-parametrizovane-zmeny','04-vyber-a-razeni-dat','05-transakce-a-vraceni-zmen']
WRONG=[
[
[("sqlite3.connect(cesta, autocommit=True)","sqlite3.connect(':memory:', autocommit=True)"),("return con.execute('SELECT sqlite_version()').fetchone()[0]","return sqlite3.sqlite_version")],
[('(jmeno,)','(jmeno.strip(),)'),('with closing(sqlite3.connect','with (sqlite3.connect')],
[("'SELECT ? + ?'","'SELECT ? - ?'"),('with closing(sqlite3.connect','with (sqlite3.connect')],
[("NOT GLOB 'sqlite_*'","NOT LIKE 'sqlite_%'"),("type = 'table'","type IN ('table', 'view')")],
[('autocommit=True','autocommit=False'),('return sqlite3.connect(cesta, autocommit=True)',"with closing(sqlite3.connect(cesta, autocommit=True)) as con:\n        return con")]
],
[
[('CHECK (kusy >= 0)','CHECK (1)'),('DEFAULT 0','DEFAULT 1')],
[('NOT NULL UNIQUE','NOT NULL'),('TEXT NOT NULL UNIQUE','TEXT UNIQUE')],
[('IN (0, 1)','IN (0, 1, 2)'),('DEFAULT 0','DEFAULT 1')],
[('popis TEXT NOT NULL','popis TEXT'),('poznamka TEXT','poznamka TEXT NOT NULL')],
[('    vytvor_kategorie(con)','    pass'),('    vytvor_kategorie(con)',"    vytvor_kategorie(con)\n    con.execute('DELETE FROM pomucky')")]
],
[
[('(nazev, kusy))','(nazev.strip(), kusy))'),('return kurzor.lastrowid','return 1')],
[('pomucky)\n','list(pomucky)[:1])\n'),('    con.executemany','    con.commit()\n    con.executemany')],
[('WHERE id = ?','WHERE id >= ?'),('return kurzor.rowcount','return kurzor.lastrowid')],
[('WHERE id = ?','WHERE id >= ?'),("return con.execute('DELETE FROM pomucky WHERE id = ?', (id_pomucky,)).rowcount","con.execute('DELETE FROM pomucky WHERE id = ?', (id_pomucky,))\n    return 1")],
[('DO NOTHING','DO UPDATE SET kusy = excluded.kusy'),('INSERT INTO pomucky','INSERT OR IGNORE INTO pomucky')]
],
[
[('ORDER BY nazev, id','ORDER BY id'),('.fetchall()','.fetchone()')],
[('WHERE id = ?','WHERE id <> ?'),('.fetchone()','.fetchall()')],
[('kusy < ?','kusy <= ?'),('ORDER BY kusy, nazev, id','ORDER BY id')],
[('kurzor.row_factory = sqlite3.Row','con.row_factory = sqlite3.Row\n    kurzor.row_factory = sqlite3.Row'),('ORDER BY id','ORDER BY nazev')],
[('(limit, posun)','(999, posun)'),(' or posun < 0','')]
],
[
[('    with con:','    if True:'),('vyzaduj_transakce(con)','pass')],
[('kusy >= ?','kusy > ?'),('SET kusy = kusy - ?','SET kusy = ?')],
[("raise ValueError('Cíl neexistuje.')",'return None'),('    with con:','    if True:')],
[("        con.execute('INSERT INTO udalosti (popis) VALUES (?)', (popis,))",'        pass'),('nove_id = kurzor.lastrowid','nove_id = 1')],
[('con.rollback()','con.commit()'),('finally:','except sqlite3.Error:')]
]
]
class SQLiteIntroTest(unittest.TestCase):
    def directory(self,stage,task=0):
        d=BASE/IDS[stage]
        return d if not task else d/'tasks'/f'task-{task+1}'

    def verify(self,d,code,expected):
        with tempfile.TemporaryDirectory() as temp:
            result=run_check(d,code,ROOT/'lib',Path(temp))
        self.assertNotIn('error',result,result)
        self.assertEqual(result['ok'],expected,(str(d),result))

    def variants(self,stage):
        for task in range(5):
            d=self.directory(stage,task);source=(d/'solution.py').read_text()
            for before,after in WRONG[stage][task]:
                # Záměna with closing za with con se týká životnosti, nikoli syntaxe.
                if before=='with closing(sqlite3.connect':
                    code=source.replace('with closing(sqlite3.connect', 'with sqlite3.connect').replace('autocommit=True)) as con:', 'autocommit=True) as con:')
                else:
                    self.assertIn(before,source,(stage,task,before));code=source.replace(before,after)
                with self.subTest(stage=stage,task=task,change=before):
                    self.verify(d,code,False)
            if stage==0:
                if task<4:code=source.replace('con.execute(', 'con.cursor().execute(')
                else:code=source.replace('autocommit=True)', 'autocommit=True, timeout=2)')
            elif stage==1:
                code=source.replace('con.execute(', 'con.cursor().execute(') if task<4 else source.replace('    vytvor_pomucky(con)\n    vytvor_kategorie(con)','    vytvor_kategorie(con)\n    vytvor_pomucky(con)')
            elif stage==2 and task==0:
                code=source.replace('VALUES (?, ?)', 'VALUES (:jmeno, :pocet)').replace('(nazev, kusy))', "{'jmeno': nazev, 'pocet': kusy})")
            elif stage==2 and task==4:
                code=source.replace('return kurzor.rowcount == 1','return bool(kurzor.rowcount)')
            elif stage==3 and task==3:
                code=source.replace('dict(radek)', '{k: radek[k] for k in radek.keys()}')
            else:
                code=source.replace('con.execute(', 'con.cursor().execute(').replace('con.executemany(', 'con.cursor().executemany(')
            self.assertNotEqual(code,source)
            self.verify(d,code,True)

    def test_connections_paths_real_queries_and_ownership(self):self.variants(0)
    def test_schema_constraints_defaults_idempotence_and_caller_transaction(self):self.variants(1)
    def test_bound_writes_ids_conflicts_and_error_propagation(self):self.variants(2)
    def test_reads_order_empty_rows_factory_and_pagination(self):self.variants(3)
    def test_atomicity_observer_rollback_and_preview(self):self.variants(4)

    def test_scope_solutions_and_prepared_schema(self):
        course=json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(next(m for m in course['modules'] if m['id']=='m01')['lessons'],IDS)
        self.assertEqual(course['requires_packages'],[])
        definitions={}
        for task in range(4):
            for n in ast.parse((self.directory(1,task)/'solution.py').read_text()).body:
                if isinstance(n,ast.FunctionDef):definitions[n.name]=ast.dump(n)
        for stage,lid in enumerate(IDS):
            view=lesson_view(ROOT/'courses','databaze',lid)
            self.assertEqual((view['kind'],view['run_timeout'],len(view['examples']),len(view['tasks']),len(view['quiz'])),('console',20,2,4,3))
            self.assertFalse(view['preview_images'])
            for task in range(5):
                d=self.directory(stage,task)
                self.assertEqual(solution_view(ROOT/'courses','databaze',lid,f'task-{task+1}')['code'],(d/'solution.py').read_text())
                self.assertTrue((d/'files/NAVOD.md').is_file())
                p=d/'files/schema.py'
                if p.is_file():
                    for n in ast.parse(p.read_text()).body:
                        if isinstance(n,ast.FunctionDef):self.assertEqual(ast.dump(n),definitions[n.name])
                if stage==1 and task<4:self.assertFalse(p.exists())

    def test_all_solutions_examples_and_teaching_snippets_run(self):
        count=0;sql_count=0
        for stage,lid in enumerate(IDS):
            d=BASE/lid
            programs=[(self.directory(stage,t),(self.directory(stage,t)/'solution.py').read_text()) for t in range(5)]
            programs += [(d,e['code']) for e in json.loads((d/'examples.json').read_text())]
            programs += [(d,s) for s in re.findall(r'\x60\x60\x60python\n(.*?)\x60\x60\x60',(d/'lesson.md').read_text(),re.S)]
            for source,code in programs:
                with self.subTest(lesson=lid,source=code[:90]),tempfile.TemporaryDirectory() as temp:
                    work=Path(temp);shutil.copytree(source/'files',work,dirs_exist_ok=True)
                    before={p.relative_to(work):p.read_bytes() for p in work.rglob('*') if p.is_file()}
                    (work/'reseni.py').write_text(code,encoding='utf-8')
                    p=subprocess.run([sys.executable,'-X','utf8','reseni.py'],cwd=work,capture_output=True,text=True,timeout=10)
                    self.assertEqual(p.returncode,0,p.stdout+p.stderr)
                    for name,data in before.items():self.assertEqual((work/name).read_bytes(),data)
                    self.assertEqual(list(work.glob('*.sqlite3')),[])
                    count+=1
            for sql in re.findall(r'\x60\x60\x60sql\n(.*?)\x60\x60\x60',(d/'lesson.md').read_text(),re.S):
                with closing(sqlite3.connect(':memory:',autocommit=True)) as con:
                    con.executescript(sql)
                    self.assertEqual(len(con.execute('PRAGMA table_info(pomucky)').fetchall()),3)
                sql_count+=1
        self.assertEqual((count,sql_count),(40,1))

    def test_real_file_reopen_and_close_rolls_back_uncommitted(self):
        # Ověření vysvětlení v lekci1/5 na skutečném souboru a druhém spojení.
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'český sklad.sqlite3'
            con=sqlite3.connect(path,autocommit=False)
            con.execute('CREATE TABLE pokus (text TEXT)')
            con.commit()
            con.execute('INSERT INTO pokus VALUES (?)',('Nedošlo k potvrzení',))
            con.close()
            with closing(sqlite3.connect(path,autocommit=True)) as other:
                self.assertEqual(other.execute('SELECT * FROM pokus').fetchall(),[])
                other.execute('INSERT INTO pokus VALUES (?)',('Žofie',))
            with closing(sqlite3.connect(path,autocommit=False)) as other:
                self.assertEqual(other.execute('SELECT text FROM pokus').fetchall(),[('Žofie',)])
            self.assertTrue(path.read_bytes().startswith(b'SQLite format 3\x00'))

if __name__=='__main__':unittest.main()
