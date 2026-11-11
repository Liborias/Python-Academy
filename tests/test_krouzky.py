"""Návaznost modelů/GUI, negativní varianty a smysluplnost studentských testů."""
import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check
from server.content import lesson_view, solution_view
BASE = ROOT/'courses/databaze/lessons'
IDS = ['11-datova-vrstva-krouzku','12-formular-a-pridani-krouzku','13-upravy-a-mazani-krouzku','14-prihlasky-a-kapacita','15-dokonceni-a-testy-evidence']


class KrouzkyTest(unittest.TestCase):
    def source(self, stage):
        return (BASE/IDS[stage]/'solution.py').read_text('utf-8')

    def check(self, stage, source, expected):
        with tempfile.TemporaryDirectory() as temp:
            r = run_check(BASE/IDS[stage], source, ROOT/'lib', Path(temp))
        self.assertNotIn('error', r, r)
        self.assertEqual(r['ok'], expected, r)

    def variants(self, stage, changes):
        source = self.source(stage)
        for before, after in changes:
            self.assertIn(before, source)
            with self.subTest(stage=stage, change=before):
                self.check(stage, source.replace(before, after), False)
        # Změna lokálních názvů ani použití kurzoru správnému řešení nevadí.
        if stage in (0, 2, 3):
            code = source.replace('self.con.execute(', 'self.con.cursor().execute(')
        elif stage == 1:
            code = source.replace('ident', 'klic')
        else:
            code = source.replace('TestEvidence', 'MojeTesty')
        self.assertNotEqual(code, source)
        self.check(stage, code, True)

    def test_all_references_accept_and_starters_reject(self):
        for stage, lid in enumerate(IDS):
            self.check(stage, self.source(stage), True)
            self.check(stage, (BASE/lid/'exercise.py').read_text(), False)

    def test_model_validation_commit_and_close(self):
        self.variants(0, [('kladna_kapacita(kapacita)\n        with', 'pass\n        with'),
                          ('nazev = cisty_nazev(nazev)', 'nazev = nazev'),
                          ('with self.con:', 'if True:'), ('self.con.close()', 'pass'),
                          ("with self.con:\n            return self.con.execute('INSERT", "if True:\n            return self.con.execute('INSERT"),
                          ('ORDER BY id', 'ORDER BY nazev')])

    def test_form_success_error_and_draft(self):
        self.variants(1, [('self.data = self.model.seznam()', 'self.data = []'),
                          ("self.w['krouzky'].delete(0, tk.END)", 'pass'),
                          ("cti_kapacitu(self.w['kapacita'].get())", '10'),
                          ("self.w['nazev'].delete(0, tk.END)", 'pass'),
                          ("self.w['stav'].configure(text='Název kroužku už existuje.')", "self.w['nazev'].delete(0, tk.END)")])

    def test_edit_delete_and_sparse_keys(self):
        self.variants(2, [('self.data[vyber[0]][0]', 'vyber[0] + 1'),
                          ('if kapacita < pocet:', 'if False:'),
                          ('WHERE id = ?', 'WHERE id >= ?'),
                          ('rowcount == 1', 'rowcount >= 0'),
                          ('ident = self.vybrane_id()', 'ident = 1')])

    def test_registration_capacity_unique_join_and_id(self):
        self.variants(3, [('if pocet >= radek[0]:', 'if pocet > radek[0]:'),
                          ('LEFT JOIN', 'JOIN'), ('COUNT(p.id)', 'COUNT(*)'),
                          ('WHERE krouzek_id = ? ORDER BY id', 'WHERE krouzek_id >= ? ORDER BY id'),
                          ("self.clenove[vyber[0]][0]", 'vyber[0] + 1'),
                          ('clen = cisty_nazev(clen)', 'clen = clen')])

    def test_student_suite_must_run_given_model_and_assert(self):
        self.variants(4, [('self.assertEqual(znovu.seznam(), [(ident, "Robotika O\'Neil", 2)])', 'pass'),
                          ('with self.assertRaises(ValueError):\n                self.model.prihlas', 'if True:\n                self.model.prihlas'),
                          ('def vytvor_sadu(Model):', 'def vytvor_sadu(ignorovany):'),
                          ('return unittest.defaultTestLoader.loadTestsFromTestCase(TestEvidence)', 'return unittest.TestSuite()')])

    def test_scope_solutions_and_exact_prior_definitions(self):
        course = json.loads((BASE.parent/'course.json').read_text())
        self.assertEqual(next(m for m in course['modules'] if m['id']=='m03')['lessons'], IDS)
        prior = {'model_zaklad.py':0, 'formular.py':1, 'upravy.py':2, 'prihlasky.py':3}
        for i, lid in enumerate(IDS):
            view = lesson_view(ROOT/'courses', 'databaze', lid)
            self.assertEqual(view['kind'], 'gui' if i in (1,2,3) else 'console')
            self.assertEqual((view['examples'], view['tasks']), ([], []))
            self.assertEqual(len(view['quiz']), 3)
            self.assertEqual(solution_view(ROOT/'courses','databaze',lid)['code'],self.source(i))
            for name, stage in prior.items():
                path = BASE/lid/'files'/name
                if path.is_file():
                    expected = [ast.dump(n) for n in ast.parse(self.source(stage)).body if isinstance(n,ast.ClassDef)]
                    got = [ast.dump(n) for n in ast.parse(path.read_text()).body if isinstance(n,ast.ClassDef)]
                    self.assertEqual(got, expected)

    def test_standalone_console_snippets_and_cli_help(self):
        import re
        for stage, lid in enumerate(IDS):
            d = BASE/lid
            programs = re.findall(r'```python\n(.*?)```', (d/'lesson.md').read_text(), re.S)
            if stage in (0,4):programs += [self.source(stage)]
            with tempfile.TemporaryDirectory() as temp:
                work = Path(temp)
                shutil.copytree(d/'files', work, dirs_exist_ok=True)
                for source in programs:
                    (work/'reseni.py').write_text(source)
                    r = subprocess.run([sys.executable, '-X','utf8','reseni.py'],cwd=work,capture_output=True,text=True,timeout=10)
                    self.assertEqual(r.returncode,0,r.stdout+r.stderr)
                (work/'reseni.py').write_text(self.source(stage))
                if stage:
                    r = subprocess.run([sys.executable,str(work/'spust_krouzky.py'),'--help'],cwd=ROOT,capture_output=True,text=True,timeout=10)
                    self.assertEqual(r.returncode,0,r.stderr)
                    self.assertIn('--db',r.stdout)
                self.assertEqual(list(work.glob('*.sqlite3')),[])

    def test_suite_references_and_model_import_have_no_side_effects(self):
        for stage,lid in enumerate(IDS):
            with tempfile.TemporaryDirectory() as temp:
                work=Path(temp);shutil.copytree(BASE/lid/'files',work,dirs_exist_ok=True)
                (work/'reseni.py').write_text(self.source(stage))
                code="""import sqlite3, tkinter
from unittest.mock import patch
with patch.object(sqlite3,'connect',side_effect=AssertionError('Import otevírá DB')), patch.object(tkinter,'Tk',side_effect=AssertionError('Import otevírá okno')):
    import reseni
"""
                r=subprocess.run([sys.executable,'-c',code],cwd=work,capture_output=True,text=True,timeout=10)
                self.assertEqual(r.returncode,0,r.stdout+r.stderr)


if __name__ == '__main__':
    unittest.main()
