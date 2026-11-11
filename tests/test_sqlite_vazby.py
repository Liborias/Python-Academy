"""SQLite6–10: chyby a alternativy, skutečné vazby/rollback a uložená konzole."""
import ast,json,os,re,shutil,sqlite3,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from server.checker import run_check
from server.content import lesson_view,solution_view
BASE=ROOT/'courses/databaze/lessons'
IDS=['06-null-typy-a-textove-filtry','07-souhrny-a-skupiny','08-cizi-klice-a-vazby','09-spojovani-tabulek','10-projekt-klubovni-evidence']
WRONG=[
[
[('poznamka IS NULL','poznamka = NULL'),('.fetchall()','.fetchone()')],
[('COALESCE(poznamka, ?)','CASE WHEN poznamka IS NULL OR length(poznamka)=0 THEN ? ELSE poznamka END'),('(nahrada,)','(nahrada.strip(),)')],
[('instr(nazev, ?) > 0','nazev LIKE ?'),('ORDER BY id','ORDER BY nazev')],
[('nazev LIKE ?','nazev = ?'),('(vzor,)','(vzor.lower(),)')],
[('volna, cele INTEGER','volna TEXT, cele INTEGER'),('autocommit=True)) as con:',"autocommit=True)) as con:")],
],
[
[('COALESCE(SUM(kusy), 0)','SUM(kusy)'),('MIN(kusy)','COALESCE(MIN(kusy),0)')],
[('COUNT(*)','COUNT(DISTINCT kusy)'),('ORDER BY kategorie','ORDER BY COUNT(*)')],
[('COUNT(poznamka)','COUNT(*)'),('COUNT(DISTINCT poznamka)','COUNT(poznamka)')],
[('SUM(kusy) >= ?','SUM(kusy) > ?'),('ORDER BY SUM(kusy) DESC','ORDER BY SUM(kusy) ASC')],
[('AVG(kusy)','AVG(NULLIF(kusy,0))'),('SELECT AVG(kusy)','SELECT COALESCE(AVG(kusy),0)')]
],
[
[('autocommit=True','autocommit=False'),("con.execute('PRAGMA foreign_keys = ON')","pass")],
[('ON DELETE SET NULL','ON DELETE CASCADE'),('ON DELETE RESTRICT','ON DELETE CASCADE')],
[('(nazev, kusy, kategorie_id)','(nazev.strip(), kusy, kategorie_id)'),('return con.execute','con.commit()\n    return con.execute')],
[('(kategorie_id, pomucka_id)','(kategorie_id, 8)'),('return con.execute','con.commit()\n    return con.execute')],
[('return con.execute','con.commit()\n    return con.execute'),("DELETE FROM kategorie WHERE id = ?","DELETE FROM kategorie WHERE id >= ?")]
],
[
[('JOIN kategorie','LEFT JOIN kategorie'),('ON p.kategorie_id = k.id','ON p.id = k.id')],
[('LEFT JOIN','JOIN'),('ORDER BY p.id','ORDER BY k.nazev')],
[('COUNT(p.id)','COUNT(*)'),('COALESCE(SUM(p.kusy), 0)','SUM(p.kusy)')],
[('NOT EXISTS','EXISTS'),(' AND v.vraceno = 0','')],
[('v.id, p.nazev','DISTINCT p.id, p.nazev'),(' AND v.vraceno = 0','')]
],
[
[('kusy = kusy - 1','kusy = kusy - 2'),('WHERE id = ? AND vraceno = 0','WHERE id = ?'),
 ('with self.con:','if True:'),('zapis_pomucku(self.con, nazev, kusy, kategorie_id)','zapis_pomucku(self.con, nazev, kusy, None)'),
 ('clen = cisty_nazev(clen)','clen = clen'),('self.con.close()','pass')]
]
]
# Druhá vada typové ukázky zapomene uzavřít vlastní spojení.
WRONG[0][4][1]=('with closing(sqlite3.connect(\':memory:\', autocommit=True)) as con:',"with sqlite3.connect(':memory:', autocommit=True) as con:")

class SQLiteVazbyTest(unittest.TestCase):
    def directory(self,stage,task=0):
        d=BASE/IDS[stage]
        return d if not task else d/'tasks'/f'task-{task+1}'
    def check_code(self,d,code,expected):
        with tempfile.TemporaryDirectory() as temp:r=run_check(d,code,ROOT/'lib',Path(temp))
        self.assertNotIn('error',r,r);self.assertEqual(r['ok'],expected,(d,r))
    def variants(self,stage):
        for task in range(1 if stage==4 else 5):
            d=self.directory(stage,task);source=(d/'solution.py').read_text()
            for before,after in WRONG[stage][task]:
                self.assertIn(before,source)
                code=source.replace(before,after);self.assertNotEqual(code,source)
                with self.subTest(stage=stage,task=task,change=before):self.check_code(d,code,False)
            if stage==0 and task==1:
                code=source.replace('COALESCE(poznamka, ?)','COALESCE(poznamka, :nahrada)').replace('(nahrada,)',"{'nahrada':nahrada}")
            elif stage==2 and task==0:
                code=source.replace('autocommit=True)','autocommit=True, timeout=2)')
            else:
                code=source.replace('con.execute(', 'con.cursor().execute(').replace('con.executemany(', 'con.cursor().executemany(')
            self.assertNotEqual(code,source)
            self.check_code(d,code,True)
    def test_null_patterns_and_real_type_affinity(self):self.variants(0)
    def test_aggregates_null_empty_groups_having_and_zero(self):self.variants(1)
    def test_foreign_keys_activation_actions_and_owner(self):self.variants(2)
    def test_join_missing_rows_counts_and_mixed_loan_history(self):self.variants(3)
    def test_project_atomic_loans_returns_persistence_and_legacy(self):self.variants(4)

    def test_scope_solutions_and_exact_prior_helpers(self):
        course=json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(next(m for m in course['modules'] if m['id']=='m02')['lessons'],IDS)
        defs={}
        for stage in [2,3]:
            for task in range(5):
                defs.update({n.name:ast.dump(n) for n in ast.parse((self.directory(stage,task)/'solution.py').read_text()).body if isinstance(n,ast.FunctionDef)})
        for stage,lid in enumerate(IDS):
            v=lesson_view(ROOT/'courses','databaze',lid)
            self.assertEqual((v['kind'],len(v['examples']),len(v['tasks']),len(v['quiz'])),('console',0 if stage==4 else 2,0 if stage==4 else 4,3))
            for task in range(1 if stage==4 else 5):
                d=self.directory(stage,task)
                self.assertEqual(solution_view(ROOT/'courses','databaze',lid,f'task-{task+1}')['code'],(d/'solution.py').read_text())
                for name in ['relacni_schema.py','operace.py','dotazy.py']:
                    p=d/'files'/name
                    if p.is_file():
                        for n in ast.parse(p.read_text()).body:
                            if isinstance(n,ast.FunctionDef):self.assertEqual(ast.dump(n),defs[n.name])
                p=d/'files/schema.py'
                if p.exists():self.assertEqual(p.read_bytes(),(BASE/'05-transakce-a-vraceni-zmen/files/schema.py').read_bytes())
        p=self.directory(4)/'files/spust_klub.py'
        self.assertIn('from reseni import Evidence',p.read_text())

    def test_standalone_solutions_examples_and_all_teaching_snippets(self):
        count=0
        for stage,lid in enumerate(IDS):
            d=BASE/lid
            programs=[(self.directory(stage,t),(self.directory(stage,t)/'solution.py').read_text()) for t in range(1 if stage==4 else 5)]
            if stage<4:programs += [(d,e['code']) for e in json.loads((d/'examples.json').read_text())]
            programs += [(d,s) for s in re.findall(r'\x60\x60\x60python\n(.*?)\x60\x60\x60',(d/'lesson.md').read_text(),re.S)]
            for directory,code in programs:
                with self.subTest(lid=lid),tempfile.TemporaryDirectory() as temp:
                    work=Path(temp);shutil.copytree(directory/'files',work,dirs_exist_ok=True)
                    before={p.relative_to(work):p.read_bytes() for p in work.rglob('*') if p.is_file()}
                    (work/'reseni.py').write_text(code,encoding='utf-8')
                    run=subprocess.run([sys.executable,'-X','utf8','reseni.py'],cwd=work,capture_output=True,text=True,timeout=10)
                    self.assertEqual(run.returncode,0,run.stdout+run.stderr)
                    for name,data in before.items():self.assertEqual((work/name).read_bytes(),data)
                    self.assertEqual(list(work.glob('*.sqlite3')),[])
                    count+=1
        self.assertEqual(count,34) # 21 řešení +8 dalších ukázek +5 úryvků

    def test_exported_cli_real_commands_reopen_and_clean_failure(self):
        d=self.directory(4)
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp)/'Klub se jménem';shutil.copytree(d/'files',work)
            (work/'reseni.py').write_bytes((d/'solution.py').read_bytes())
            entry=str(work/'spust_klub.py');path=work/'klub.sqlite3'
            def cli(*args,expected=0):
                p=subprocess.run([sys.executable,'-X','utf8',entry,*args],cwd=temp,capture_output=True,text=True,timeout=10)
                self.assertEqual(p.returncode,expected,p.stdout+p.stderr);return p.stdout
            cli('--help');self.assertFalse(path.exists())
            self.assertIn('Kategorie ID: 1',cli('kategorie','Sport'))
            self.assertIn('Pomůcka ID: 1',cli('pomucka',"Míč O'Neil",'2','--kategorie','1'))
            self.assertIn('Výpůjčka ID: 1',cli('pujcit','1','Žofie'))
            self.assertIn('Žofie',cli('vypujcky'))
            self.assertIn('Vráceno: True',cli('vratit','1'))
            self.assertIn('Vráceno: False',cli('vratit','1'))
            self.assertIn('Chyba:',cli('pomucka','Chybná','1','--kategorie','999',expected=2))
            self.assertIn('Chyba:',cli('pomucka','Záporná','-1',expected=2))
            output=cli('prehled')
            self.assertIn('(1, "Míč O\'Neil", 2, \'Sport\')',output)
            self.assertEqual(cli('vypujcky'),'')
            other=work/'jiný.sqlite3'
            cli('--db',str(other),'kategorie','Jiná')
            with sqlite3.connect(other) as con:self.assertEqual(con.execute('SELECT nazev FROM kategorie').fetchall(),[('Jiná',)])
            with sqlite3.connect(path) as con:
                self.assertEqual(con.execute('SELECT kusy FROM pomucky').fetchall(),[(2,)])
                self.assertEqual(con.execute('SELECT vraceno FROM vypujcky').fetchall(),[(1,)])

    def test_connection_setup_failure_closes_its_own_handle(self):
        d=self.directory(2)
        script="""import sqlite3
from unittest.mock import patch
import reseni
original=sqlite3.connect
opened=[]
class PrazdneNastaveni(sqlite3.Connection):
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw)
        self.autocommit=False
        self.closed=False
    def close(self):
        self.closed=True
        super().close()
def connect(*a,**kw):
    kw['factory']=PrazdneNastaveni
    c=original(*a,**kw);opened.append(c);return c
with patch.object(sqlite3,'connect',side_effect=connect):
    try:reseni.spojeni_s_vazbami(':memory:')
    except RuntimeError:pass
    else:raise AssertionError('Nastavení vazeb se nemělo podařit.')
assert opened and all(c.closed for c in opened)
"""
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp);shutil.copytree(d/'files',work,dirs_exist_ok=True)
            (work/'reseni.py').write_bytes((d/'solution.py').read_bytes())
            p=subprocess.run([sys.executable,'-c',script],cwd=work,capture_output=True,text=True,timeout=10)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)

if __name__=='__main__':unittest.main()
