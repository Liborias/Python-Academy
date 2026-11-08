"""Výběr kontrol, stará data a oddělené pracovní soubory úkolů."""
import http.client
import json
import shutil
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server
from server.checker import lesson_dir, run_check
from server.content import lesson_view, workspace_file


class TasksTest(unittest.TestCase):
    def test_scope_and_public_content(self):
        total = 0
        for directory in (ROOT / 'courses').glob('*/lessons/*'):
            if not (directory / 'lesson.md').exists():
                continue
            cid, lid = directory.parent.parent.name, directory.name
            view = lesson_view(ROOT / 'courses', cid, lid)
            tasks = view['tasks']
            expected = cid in {'zaklady', 'pandas'} and (directory / 'examples.json').exists()
            self.assertEqual(len(tasks), 4 if expected else 0, str(directory))
            total += len(tasks)
            for task in tasks:
                self.assertNotIn('solution', task)
                self.assertNotIn('check', task)
                self.assertTrue(task['md'] and task['exercise'])
        self.assertEqual(total, 196)

    def test_selection_and_traversal(self):
        root = ROOT / 'courses'
        lid = '01-prvni-program'
        original = lesson_dir(root, 'zaklady', lid)
        self.assertEqual(lesson_dir(root, 'zaklady', lid, 'task-1'), original)
        self.assertEqual(lesson_dir(root, 'zaklady', lid, 'task-2'), original / 'tasks/task-2')
        for bad in ['../solution', '../../01', 'task-6', [], {}, 3]:
            self.assertIsNone(lesson_dir(root, 'zaklady', lid, bad))
            self.assertIsNone(workspace_file(ROOT, 'zaklady', lid, bad))
        self.assertIsNone(lesson_dir(root, 'pygame-1', '01-prvni-okno', 'task-2'))
        self.assertEqual(workspace_file(ROOT, 'zaklady', lid), ROOT / 'workspace/zaklady' / lid / 'reseni.py')

    def test_checks_reject_constant_and_accept_alternative(self):
        with tempfile.TemporaryDirectory() as work:
            for lid in ['12-parametry-a-return','13-vychozi-hodnoty','14-rozsah-platnosti','19-pocitani-ve-slovniku','25-modul-random','39-opakovani-oprava-kodu']:
                d = lesson_dir(ROOT / 'courses', 'zaklady', lid, 'task-2')
                code = (d / 'solution.py').read_text('utf-8')
                import ast
                func = next(n for n in ast.parse(code).body if isinstance(n, ast.FunctionDef))
                mutant = '\n'.join(line for line in code.splitlines() if line.startswith(('import ', 'from ')))
                mutant += f'\ndef {func.name}(*args, **kwargs):\n    return 0\n'
                self.assertFalse(run_check(d, mutant, ROOT / 'lib', Path(work)).get('ok'), lid)
            d = lesson_dir(ROOT / 'courses', 'zaklady', '15-funkce-a-seznamy', 'task-2')
            # Správné řešení bez append, zachovává pořadí i původní seznam.
            alternative = 'def bez_nul(data):\n    return [x for x in data if x != 0]\n'
            self.assertTrue(run_check(d, alternative, ROOT / 'lib', Path(work)).get('ok'))

    def test_http_check_and_workspace_are_independent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / 'lib', root / 'lib')
            srv = create_server(root, '127.0.0.1', 0, courses_dir=ROOT / 'courses')
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            try:
                def req(path, body=None, token=True):
                    conn = http.client.HTTPConnection(*srv.server_address, timeout=30)
                    headers = {'Content-Type':'application/json'}
                    if token: headers['X-Dilna-Token'] = srv.token
                    try:
                        conn.request('POST' if body is not None else 'GET', path, json.dumps(body) if body is not None else None, headers)
                        response = conn.getresponse()
                        return response.status, json.loads(response.read())
                    finally: conn.close()
                base = {'course':'zaklady','lesson':'01-prvni-program'}
                for task in [None, 'task-2', 'task-3']:
                    fields = {**base, **({'task':task} if task else {})}
                    d = lesson_dir(ROOT / 'courses', 'zaklady', base['lesson'], task)
                    solution = (d / 'solution.py').read_text('utf-8')
                    status, result = req('/api/check', {**fields, 'code':solution})
                    self.assertEqual(status, 200)
                    self.assertTrue(result['ok'], result)
                    status, saved = req('/api/workspace/save', {**fields,'code':solution})
                    self.assertEqual(status, 200)
                    self.assertEqual(Path(saved['path']).read_text('utf-8'), solution)
                wrong = (lesson_dir(ROOT / 'courses', 'zaklady', base['lesson'], 'task-2') / 'solution.py').read_text('utf-8')
                self.assertFalse(req('/api/check', {**base,'task':'task-3','code':wrong})[1]['ok'])
                self.assertEqual(req('/api/check', {**base,'task':'../task-2','code':''})[0], 404)
                self.assertEqual(req('/api/check', {**base,'task':'task-2','code':''}, token=False)[0], 401)
                for task in [None, 'task-2','task-3']:
                    status, data = req('/api/workspace?course=zaklady&lesson=01-prvni-program'+('&task='+task if task else ''))
                    d = lesson_dir(ROOT / 'courses','zaklady',base['lesson'],task)
                    self.assertEqual(data['code'], (d/'solution.py').read_text('utf-8'))
            finally:
                srv.runs.stop_all(); srv.shutdown(); srv.server_close()


if __name__ == '__main__':
    unittest.main()
