"""Řešení všech kurzů: dostupnost, přesný výběr a samostatné čtecí API."""
import http.client
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server
from server.content import lesson_view, solution_view


class SolutionsTest(unittest.TestCase):
    def test_availability_without_eager_source(self):
        originals = extras = 0
        for directory in (ROOT/'courses').glob('*/lessons/*'):
            if not (directory/'lesson.md').exists():
                continue
            cid, lid = directory.parent.parent.name, directory.name
            view = lesson_view(ROOT/'courses', cid, lid)
            self.assertEqual(view['has_solution'], (directory/'solution.py').is_file())
            self.assertNotIn('solution', view)
            self.assertNotIn('code', view)
            originals += view['has_solution']
            for task in view['tasks']:
                self.assertTrue(task['has_solution'])
                self.assertNotIn('solution', task)
                self.assertNotIn('code', task)
                self.assertNotIn('check', task)
                extras += task['has_solution']
        self.assertEqual((originals, extras), (235, 308))

    def test_every_reference_matches_selected_task(self):
        count = 0
        for directory in (ROOT/'courses').glob('*/lessons/*'):
            if not (directory/'solution.py').is_file():
                continue
            cid = directory.parent.parent.name
            lid = directory.name
            original = solution_view(ROOT/'courses', cid, lid)
            self.assertEqual(original, solution_view(ROOT/'courses', cid, lid, 'task-1'))
            for task, source in [('task-1', directory), *[(p.name, p) for p in (directory/'tasks').glob('task-*')]]:
                result = solution_view(ROOT/'courses', cid, lid, task)
                self.assertEqual(result, {'course': cid, 'lesson': lid, 'task': task, 'code': (source/'solution.py').read_text('utf-8')})
                count += 1
        self.assertEqual(count, 543)

    def test_invalid_selection_guides_and_planned_courses(self):
        guides = [(d.parent.parent.name,d.name,None) for d in (ROOT/'courses/priprava/lessons').iterdir()]
        for cid, lid, task in [*guides, ('pandas','01-test',None), ('databaze','01-test',None),
                               ('oop','17-navrh-expedicniho-centra','task-2'),
                               ('tkinter-api','../27-cesty-a-klavesove-zkratky',None),
                               ('../zaklady', '01-prvni-program', None), ('zaklady', '../01-prvni-program', None),
                               ('zaklady', '99-neexistuje', None), ('zaklady', '01-prvni-program', '../solution'),
                               ('zaklady', '01-prvni-program', 'task-6'), ('zaklady', '32-projekt-hadej-planetu', 'task-2'),
                               ('zaklady', '01-prvni-program', []), ('zaklady', '01-prvni-program', 2)]:
            with self.subTest(cid=cid, lid=lid, task=task):
                self.assertIsNone(solution_view(ROOT/'courses', cid, lid, task))

    def test_missing_or_empty_solution_is_unavailable(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            d = base/'tkinter-api/lessons/01-test'
            d.mkdir(parents=True)
            (d/'lesson.md').write_text('Zadání', encoding='utf-8')
            (d/'check.py').write_text('# Kontrola', encoding='utf-8')
            for source in (None, ' \n'):
                if source is not None:
                    (d/'solution.py').write_text(source, encoding='utf-8')
                self.assertFalse(lesson_view(base, 'tkinter-api', '01-test')['has_solution'])
                self.assertIsNone(solution_view(base, 'tkinter-api', '01-test'))

    def test_http_selection_and_read_guards(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            srv = create_server(root, '127.0.0.1', 0, courses_dir=ROOT/'courses')
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            try:
                before = sorted(str(p.relative_to(root)) for p in root.rglob('*'))
                def get(path, headers=None):
                    conn = http.client.HTTPConnection(*srv.server_address, timeout=10)
                    try:
                        conn.request('GET', path, headers=headers or {})
                        response = conn.getresponse()
                        return response.status, json.loads(response.read())
                    finally:
                        conn.close()
                query = '/api/solution?course=zaklady&lesson=01-prvni-program'
                for suffix, task in [('', None), ('&task=task-1', 'task-1'), ('&task=task-3', 'task-3')]:
                    status, body = get(query+suffix)
                    self.assertEqual(status, 200)
                    self.assertEqual(body, solution_view(ROOT/'courses', 'zaklady', '01-prvni-program', task))
                for directory in (ROOT/'courses').glob('*/lessons/*'):
                    if not (directory/'solution.py').is_file():
                        continue
                    cid,lid=directory.parent.parent.name,directory.name
                    path=f'/api/solution?course={cid}&lesson={lid}'
                    status,body=get(path)
                    self.assertEqual(status,200,path)
                    self.assertEqual(body,solution_view(ROOT/'courses',cid,lid))
                for path in (query+'&task=..%2Fsolution', query+'&task=task-6', '/api/solution',
                             '/api/solution?course=oop&lesson=17-navrh-expedicniho-centra&task=task-2',
                             '/api/solution?course=tkinter-api&lesson=..%2F27-cesty-a-klavesove-zkratky'):
                    self.assertEqual(get(path)[0], 404)
                self.assertEqual(get(query, {'Origin':'https://cizi.example'})[0], 403)
                self.assertEqual(get(query, {'Host':'cizi.example'})[0], 403)
                self.assertEqual(sorted(str(p.relative_to(root)) for p in root.rglob('*')), before, 'Čtení vzoru nemá měnit pracovní soubory')
            finally:
                srv.runs.stop_all()
                srv.shutdown()
                srv.server_close()


if __name__ == '__main__':
    unittest.main()
