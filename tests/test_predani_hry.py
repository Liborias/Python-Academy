"""Závěr Pygame 2: skutečné scénáře, užitečnost testů, soubory a GUI projekt."""
import ast
import json
import os
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
BASE=ROOT/'courses/pygame-2/lessons'
IDS=['26-rizene-herni-scenare','27-vlastni-testy-hry','28-vysledky-v-json','29-priprava-a-baleni-hry','30-kuryrska-smena-a-predani']
WRONG=[
[
[('Kolo(seed)','Kolo(23)'),('stopa = [snimek(kolo)]','stopa = []')],
[('cast = min(krok, zbyva)','cast = krok'),('zbyva > 1e-12','zbyva > 0.02')],
[('vysledek.append(tuple(smer))','vysledek.append(zmeny.get(snimek_cislo, (0, 0)))'),('vysledek.append(tuple(smer))','vysledek.append((0, 0))')],
[('draha += math.dist','draha = math.dist'),("'kroky': max(0, len(stopa) - 1)","'kroky': len(stopa)")],
[('kroky = list(kroky)','kroky = kroky'),('return prehraj(seed, kroky), prehraj(seed, kroky)','stopa = prehraj(seed, kroky)\n    return stopa, stopa')]
],
[],
[
[("type(zaznam.get('body')) is int","isinstance(zaznam.get('body'), int)"),("zaznam['body'] >= 0","True")],
[("'jmeno': z['jmeno'].strip()","'jmeno': z['jmeno']"),('if not isinstance(data, list):','if False:')],
[("not z['uspech'], -z['body']","not z['uspech'], z['body']"),(')[:limit]',')')],
[("type(dokument.get('verze')) is not int","not isinstance(dokument.get('verze'), int)"),('FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError','OSError, json.JSONDecodeError, UnicodeDecodeError')],
[('os.replace(docasna, cesta)',"cesta.write_text('', encoding='utf-8')\n        os.replace(docasna, cesta)"),("docasna.unlink(missing_ok=True)","pass")]
],
[
[('spustitelny if zmrazeno else soubor','soubor'),('.resolve().parent','.resolve()')],
[('.is_file()','.exists()'),('return sorted(jmeno for jmeno in povinne if not (koren / jmeno).is_file())','return list(povinne)')],
[("'-X', 'utf8'","'-X', 'ascii'"),("str(skript)]","str(skript).split()]")],
[("'--onedir'","'--onefile'"),("jmeno[0].isalpha()","True")],
[("'-p', 'test_*.py'","'-p', '*.py'"),("testy.is_dir()","testy.exists() or True")]
],
[
[('self.rychlost = rychlost','self.rychlost = 260'),
 ('self.zapsane_kolo is self.kolo','False'),
 ("self.vysledky = poradi","self.vysledky = []"),
 ("except OSError:","except FileNotFoundError:"),
 ("poradi = serad_vysledky([*self.vysledky, novy], 5)","poradi = serad_vysledky([*self.vysledky, novy], 99)")]
]
]
# Pro vlastní unittest hodnotíme odlišení modelu od vad, nikoli názvy metod.
BAD_SUITES=[
"""import unittest
def sestav_sadu():
    return unittest.TestSuite()
""",
"""import unittest
class JenSoucet(unittest.TestCase):
    def test_nesouvisi_s_hrou(self):
        self.assertEqual(2+3,5)
def sestav_sadu():
    return unittest.defaultTestLoader.loadTestsFromTestCase(JenSoucet)
""",
"""import unittest
class VzdySelze(unittest.TestCase):
    def test_chybny_predpoklad(self):
        self.fail('Nezávisle na hře')
def sestav_sadu():
    return unittest.defaultTestLoader.loadTestsFromTestCase(VzdySelze)
"""
]
CORRECT=[
[('stopa = [snimek(kolo)]','stopa = []\n    stopa.append(snimek(kolo))')],
[('cast = min(krok, zbyva)','cast = zbyva if zbyva < krok else krok')],
[('smer = tuple(zmeny[snimek_cislo])','smer = (*zmeny[snimek_cislo],)')],
[('math.dist(pred[\'pozice\'], po[\'pozice\'])',"(pygame.Vector2(po['pozice']) - pred['pozice']).length()")],
[('kroky = list(kroky)','kroky = tuple(kroky)')]
]
class PredaniHryTest(unittest.TestCase):
    def directory(self,stage,task=0):
        d=BASE/IDS[stage]
        return d if not task else d/'tasks'/f'task-{task+1}'

    def check_variant(self,d,code,expected):
        with tempfile.TemporaryDirectory() as temp:
            result=run_check(d,code,ROOT/'lib',Path(temp))
        self.assertNotIn('error',result,result)
        self.assertEqual(result['ok'],expected,(str(d),result))

    def variants(self,stage):
        for task in range(1 if stage==4 else 5):
            d=self.directory(stage,task)
            source=(d/'solution.py').read_text()
            for before,after in WRONG[stage][task]:
                with self.subTest(stage=stage,task=task,change=before):
                    self.assertIn(before,source)
                    self.check_variant(d,source.replace(before,after),False)
            alternatives={
                0:[('stopa = [snimek(kolo)]','stopa = list((snimek(kolo),))'),('vysledek = []','vysledek = list()'),('smer = tuple(zmeny[snimek_cislo])','smer = (*zmeny[snimek_cislo],)'),("'kroky': max(0, len(stopa) - 1)","'kroky': len(stopa) - 1 if stopa else 0"),('kroky = list(kroky)','kroky = tuple(kroky)')],
                2:[("type(zaznam.get('uspech')) is bool","isinstance(zaznam.get('uspech'), bool)"),('return []','return list()'),("not z['uspech']","-int(z['uspech'])"),("Path(cesta).read_text(encoding='utf-8')","Path(cesta).read_bytes().decode('utf-8')"),('docasna.unlink(missing_ok=True)','if docasna.exists(): docasna.unlink()')],
                3:[('Path(zdroj).resolve().parent','Path(zdroj).absolute().resolve().parent'),('sorted(jmeno for jmeno in povinne if not (koren / jmeno).is_file())','sorted([jmeno for jmeno in povinne if not (koren / jmeno).is_file()])'),('skript.suffix.lower()','skript.suffix.casefold()'),("c.isalnum() or c in '_-'","c in '_-' or c.isalnum()"),('not testy.is_dir()','not (testy.exists() and testy.is_dir())')],
                4:[('self.kolo.hrac.rychlost = self.rychlost',"setattr(self.kolo.hrac, 'rychlost', self.rychlost)")]
            }
            before,after=alternatives[stage][task]
            self.assertIn(before,source)
            code=source.replace(before,after)
            self.check_variant(d,code,True)

    def test_scenarios_and_independent_traces(self):
        self.variants(0)
        for task,changes in enumerate(CORRECT):
            d=self.directory(0,task);code=(d/'solution.py').read_text()
            for a,b in changes:
                self.assertIn(a,code);code=code.replace(a,b)
            self.check_variant(d,code,True)

    def test_students_tests_distinguish_correct_and_faulty_models(self):
        for task in range(5):
            d=self.directory(1,task);source=(d/'solution.py').read_text()
            self.check_variant(d,source,True)
            before=next(line for line in source.splitlines() if 'return unittest.defaultTestLoader' in line)
            after=before.replace('return unittest.defaultTestLoader','return unittest.TestSuite(unittest.defaultTestLoader')+')'
            self.check_variant(d,source.replace(before,after),True)
            for code in BAD_SUITES:
                with self.subTest(task=task,bad=code):
                    self.check_variant(d,code,False)

    def test_json_validation_order_read_and_atomic_write(self):self.variants(2)
    def test_delivery_paths_arguments_and_no_side_effects(self):self.variants(3)
    def test_final_project_persists_once_and_handles_errors(self):self.variants(4)

    def test_scope_exact_sources_and_previous_model(self):
        expected={}
        for p in [BASE/'25-droni-hra-pauza-a-vysledek/files/predchozi.py',BASE/'25-droni-hra-pauza-a-vysledek/solution.py']:
            expected.update({n.name:ast.dump(n) for n in ast.parse(p.read_text()).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))})
        course=json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(next(m for m in course['modules'] if m['id']=='m06')['lessons'],IDS)
        all_definitions={}
        for stage in [2,3]:
            for task in range(5):
                all_definitions.update({n.name:ast.dump(n) for n in ast.parse((self.directory(stage,task)/'solution.py').read_text()).body if isinstance(n,ast.FunctionDef)})
        for stage,lid in enumerate(IDS):
            view=lesson_view(ROOT/'courses','pygame-2',lid)
            self.assertEqual((view['kind'],len(view['examples']),len(view['tasks']),len(view['quiz'])),('gui' if stage==4 else 'console',0 if stage==4 else 2,0 if stage==4 else 4,3))
            for task in range(1 if stage==4 else 5):
                d=self.directory(stage,task)
                self.assertEqual(solution_view(ROOT/'courses','pygame-2',lid,f'task-{task+1}')['code'],(d/'solution.py').read_text())
                if stage!=2:
                    actual={n.name:ast.dump(n) for n in ast.parse((d/'files/model_hry.py').read_text()).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
                    self.assertEqual(actual,expected)
                if stage in (3,4):
                    entry=ast.parse((d/'files/hra.py').read_text())
                    self.assertFalse(any(isinstance(n,ast.ClassDef) for n in entry.body))
                    self.assertTrue(any(isinstance(n,ast.ImportFrom) and n.module=='model_hry' and any(a.name=='Hra' for a in n.names) for n in entry.body))
                for name in ['vysledky.py','vysledky_podklady.py','cesty.py']:
                    p=d/'files'/name
                    if p.exists():
                        for n in ast.parse(p.read_text()).body:
                            if isinstance(n,ast.FunctionDef):self.assertEqual(ast.dump(n),all_definitions[n.name])

    def test_standalone_solutions_examples_snippets_and_clean_copy(self):
        count=0
        for stage,lid in enumerate(IDS[:4]):
            d=BASE/lid
            programs=[(self.directory(stage,task),(self.directory(stage,task)/'solution.py').read_text()) for task in range(5)]
            programs += [(d,e['code']) for e in json.loads((d/'examples.json').read_text())]
            programs += [(d,s) for s in re.findall(r'\x60\x60\x60python\n(.*?)\x60\x60\x60',(d/'lesson.md').read_text(),re.S)]
            for source,code in programs:
                with self.subTest(lesson=lid),tempfile.TemporaryDirectory() as temp:
                    work=Path(temp);shutil.copytree(source/'files',work,dirs_exist_ok=True)
                    before={p.relative_to(work):p.read_bytes() for p in work.rglob('*') if p.is_file()}
                    (work/'reseni.py').write_text(code)
                    p=subprocess.run([sys.executable,'-X','utf8','reseni.py'],cwd=work,capture_output=True,text=True,timeout=15)
                    self.assertEqual(p.returncode,0,p.stdout+p.stderr)
                    for name,data in before.items():self.assertEqual((work/name).read_bytes(),data)
                    count+=1
        self.assertEqual(count,32) # 20 řešení + 8 dalších ukázek + 4 úryvky
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp)/'čistá složka';shutil.copytree(self.directory(4)/'files',work)
            (work/'reseni.py').write_bytes((self.directory(4)/'solution.py').read_bytes())
            result=subprocess.run([sys.executable,str(work/'over_projekt.py')],cwd=temp,capture_output=True,text=True,timeout=15)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertIn('Ran 6 tests',result.stderr)
            self.assertIn('OK',result.stderr)
            snippet=re.search(r'\x60\x60\x60python\n(.*?)\x60\x60\x60',(self.directory(4)/'lesson.md').read_text(),re.S)[1]
            result=subprocess.run([sys.executable,'-c',snippet],cwd=work,capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_final_entrypoint_real_loop_png_and_readonly_helpers(self):
        from PIL import Image
        d=self.directory(4)
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp);shutil.copytree(d/'files',work,dirs_exist_ok=True)
            before={p.relative_to(work):p.read_bytes() for p in work.rglob('*') if p.is_file()}
            (work/'reseni.py').write_bytes((d/'solution.py').read_bytes())
            (work/'spec.json').write_text(json.dumps({'frames':100,'held':{'0':['K_RIGHT']},'events':{'0':[{'type':'KEYDOWN','key':'K_SPACE'}],'5':[{'type':'KEYDOWN','key':'K_p'}],'7':[{'type':'KEYDOWN','key':'K_p'}],'9':[{'type':'KEYDOWN','key':'K_r'}],'80':[{'type':'QUIT'}]}}))
            p=subprocess.run([sys.executable,str(ROOT/'lib/dilna_check/pgrun.py'),'reseni.py','spec.json','out.json'],cwd=work,capture_output=True,text=True,timeout=15)
            self.assertEqual(p.returncode,0,p.stderr)
            result=json.loads((work/'out.json').read_text());self.assertIsNone(result['error']);self.assertTrue(result['ended'])
            with Image.open(work/'droni.png') as img:img.load();self.assertEqual(img.size,(720,540))
            self.assertFalse((work/'data/vysledky.json').exists())
            for name,data in before.items():self.assertEqual((work/name).read_bytes(),data)
            code=(d/'solution.py').read_text().split('# Samostatné spuštění')[0]
            self.check_variant(d,code,False)

if __name__=='__main__':unittest.main()
