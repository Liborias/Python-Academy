"""Účty 21–25: skutečné odvození, izolace sezení a přenos přes uložené CLI."""
import ast
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
IDS=['21-scrypt-sul-a-overeni-hesla','22-registrace-a-jedinecnost','23-mistni-prihlaseni-a-poznamky','24-volitelne-cteni-textu-offline','25-zlib-base64-a-prenos-poznamek']


class MistniUctyTest(unittest.TestCase):
    def source(self,i):return (BASE/IDS[i]/'solution.py').read_text()
    def check(self,i,code,expected):
        with tempfile.TemporaryDirectory() as temp:r=run_check(BASE/IDS[i],code,ROOT/'lib',Path(temp))
        self.assertNotIn('error',r,r);self.assertEqual(r['ok'],expected,r)
    def variants(self,i,changes):
        source=self.source(i)
        for a,b in changes:
            self.assertIn(a,source)
            with self.subTest(stage=i,change=a):self.check(i,source.replace(a,b),False)
        if i==0:
            good=source.replace('import hashlib','from hashlib import scrypt').replace('hashlib.scrypt','scrypt').replace('import hmac','from hmac import compare_digest').replace('hmac.compare_digest','compare_digest')
        elif i in (1,2):good=source.replace('self.con.execute(','self.con.cursor().execute(')
        elif i==3:good=re.sub(r'\bprikaz\b','argv',source)
        else:good=source.replace('dekoder','proud')
        self.assertNotEqual(good,source);self.check(i,good,True)

    def test_references_and_starters(self):
        for i,lid in enumerate(IDS):
            self.check(i,self.source(i),True);self.check(i,(BASE/lid/'exercise.py').read_text(),False)

    def test_scrypt_salt_exact_password_and_profile(self):
        self.variants(0,[('secrets.token_bytes(16)',"b'0'*16"),('data = over_heslo_text(heslo)','data = over_heslo_text(heslo.strip())'),
                         ('if not over_zaznam(zaznam):','if False:'),('hmac.compare_digest(skutecny, ocekavany)','skutecny == ocekavany')])

    def test_registration_normalization_unique_and_commit(self):
        self.variants(1,[('vytvor_zaznam(heslo)', "vytvor_zaznam('Jiná fiktivní fráze!')"),('jmeno = jmeno_uctu(jmeno)','jmeno = jmeno.strip()'),
                         ("with self.con:\n            return self.con.execute('INSERT", "if True:\n            return self.con.execute('INSERT"),
                         ('self.con.close()','pass')])

    def test_session_owner_logout_and_atomic_batch(self):
        self.variants(2,[('WHERE uzivatel_id=? ORDER BY id','WHERE uzivatel_id>=? ORDER BY id'),
                         ('self.uzivatel = None\n        self.uzivatel = self.ucty.prihlaseni(jmeno, heslo)','nova = self.ucty.prihlaseni(jmeno, heslo)\n        if nova is not None: self.uzivatel = nova'),
                         ('if self.uzivatel is None:','if False:'),
                         ('texty = over_poznamky(texty)','texty = texty'),('with self.con:\n            self.con.executemany','if True:\n            self.con.executemany')])

    def test_speech_preview_stdin_timeout_and_errors(self):
        self.variants(3,[('if not mluv:','if False:'),('input=text','input=text.strip()'),('timeout=15','timeout=None'),("errors='replace'","errors='strict'"),
                         ("return 'nedostupne'", "return 'precteno'")])

    def test_codec_limits_truncation_trailing_data_and_utf8(self):
        self.variants(4,[('zlib.compress(data)','data'),('return text.decode(\'utf-8\')',"return text.decode('utf-8').strip()"),
                         ('or dekoder.unused_data','or False'),('not dekoder.eof','False'),
                         ('decompress(data, MAX_TEXT+1)','decompress(data)'),('if len(text)>MAX_TEXT','if len(text)>MAX_TEXT*2')])

    def test_scope_prior_definitions_and_solutions(self):
        course=json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(next(m for m in course['modules'] if m['id']=='m05')['lessons'],IDS)
        for i,lid in enumerate(IDS):
            v=lesson_view(ROOT/'courses','databaze',lid)
            self.assertEqual((v['kind'],len(v['examples']),len(v['tasks']),len(v['quiz'])),('console',2 if i in (0,4) else 0,0,3))
            self.assertEqual(solution_view(ROOT/'courses','databaze',lid)['code'],self.source(i))
            for name,prior in [('hesla.py',0),('ucty.py',1),('sezeni.py',2)]:
                p=BASE/lid/'files'/name
                if p.exists():
                    def definitions(code):return [ast.dump(n) for n in ast.parse(code).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
                    self.assertEqual(definitions(p.read_text()),definitions(self.source(prior)))

    def test_console_examples_and_markdown_snippets(self):
        count=0
        for i,lid in enumerate(IDS):
            d=BASE/lid;sources=[self.source(i),*re.findall(r'```python\n(.*?)```',(d/'lesson.md').read_text(),re.S)]
            if (d/'examples.json').exists():sources += [v['code'] for v in json.loads((d/'examples.json').read_text())]
            for source in sources:
                with tempfile.TemporaryDirectory() as temp:
                    w=Path(temp);shutil.copytree(d/'files',w,dirs_exist_ok=True);(w/'reseni.py').write_text(source,encoding='utf-8')
                    r=subprocess.run([sys.executable,'-X','utf8','reseni.py'],cwd=w,capture_output=True,text=True,timeout=15)
                    self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertEqual(list(w.glob('*.sqlite3')),[])
                    count+=1
        self.assertEqual(count,14)

    def test_saved_cli_real_database_getpass_boundary_and_transfer(self):
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp)/'Moje účty';shutil.copytree(BASE/IDS[4]/'files',work);(work/'reseni.py').write_text(self.source(4))
            driver="""import sys,runpy,getpass
from pathlib import Path
entry=sys.argv[1];sys.path.insert(0,str(Path(entry).parent));sys.argv=sys.argv[1:]
getpass.getpass=lambda prompt='': 'Fiktivní heslo do testu!'
runpy.run_path(entry,run_name='__main__')
"""
            def cli(*args,stdin='',expected=0):
                r=subprocess.run([sys.executable,'-X','utf8','-c',driver,str(work/'spust_ucty.py'),*args],input=stdin,cwd=temp,capture_output=True,text=True,timeout=15)
                self.assertEqual(r.returncode,expected,r.stdout+r.stderr);self.assertNotIn('Fiktivní heslo do testu!',r.stdout+r.stderr);return r.stdout
            cli('--help');self.assertFalse((work/'ucty.sqlite3').exists())
            self.assertIn('Účet ID: 1',cli('registrace','Zofie'))
            cli('registrace','ZOFIE',expected=2)
            self.assertIn('Poznámka uložena.',cli('prihlaseni','Zofie',stdin='2\nČeská poznámka; ukázka\n3\n'))
            packed=work/'poznamky.txt'
            self.assertIn('Počet poznámek: 1',cli('export','Zofie',str(packed)))
            self.assertTrue(packed.read_text().startswith('z1:'))
            self.assertIn('Počet poznámek: 1',cli('import','Zofie',str(packed)))
            out=cli('prihlaseni','Zofie',stdin='1\n3\n');self.assertEqual(out.count('Česká poznámka; ukázka'),2)
            self.assertIn('Účet ID: 2',cli('registrace','Ada'))
            self.assertNotIn('Česká poznámka',cli('prihlaseni','Ada',stdin='1\n3\n'))
            cli('export','Zofie',str(work/'ucty.sqlite3'),expected=2)
            packed.write_text('z1:poskozene');cli('import','Zofie',str(packed),expected=2)
            self.assertEqual(list(work.glob('.bmi-*')),[])


if __name__=='__main__':unittest.main()
