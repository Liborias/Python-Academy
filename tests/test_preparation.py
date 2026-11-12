"""Profily kurzů, nové dokumenty, koncept a skutečné rozdělení závislostí."""
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
from server.preparation import PROFILES, course_preparation
from tools.setup_env import PACKAGES, OPTIONAL_PACKAGES, wanted
from tools import validate_courses as validator


class PreparationTest(unittest.TestCase):
    def test_all_courses_have_consistent_profile(self):
        catalog = json.loads((ROOT / 'courses/catalog.json').read_text())['courses']
        self.assertEqual(catalog[0]['id'], 'priprava')
        self.assertEqual(catalog[0]['status'], 'concept')
        self.assertEqual(set(PROFILES), {c['id'] for c in catalog})
        for course in catalog:
            profile = course_preparation(course['id'])
            self.assertEqual(profile['packages'], wanted(course['id']))
            self.assertEqual(profile['optional_packages'], OPTIONAL_PACKAGES.get(course['id'], []))
            compile(profile['verify'], '<verify>', 'exec')
        self.assertIsNone(course_preparation('../zaklady'))

    def test_optional_packages_are_opt_in(self):
        self.assertEqual(wanted('tkinter-api'), ['requests', 'aiosmtpd>=1.4.6,<2'])
        self.assertEqual(wanted('databaze'), [])
        self.assertIn('pyinstaller', wanted('tkinter-api', extras=True))
        self.assertIn('qrcode[pil]>=8.2,<9', wanted('databaze', extras=True))
        self.assertNotIn('pyinstaller', wanted('all'))
        self.assertEqual(wanted('pygame-1,pygame-2'), ['pygame-ce'])

    def test_guides_have_structure_without_fake_code_checks(self):
        course = json.loads((ROOT / 'courses/priprava/course.json').read_text())
        ids = [lid for m in course['modules'] for lid in m['lessons']]
        self.assertEqual(len(ids), 15)
        for lid in ids:
            with self.subTest(lesson=lid), tempfile.TemporaryDirectory() as work:
                before = len(validator.errors)
                validator.validate_lesson(ROOT / 'courses/priprava', lid, Path(work))
                self.assertEqual(validator.errors[before:], [])
        with tempfile.TemporaryDirectory() as work:
            path = Path(work) / 'lessons' / '01-broken'
            path.mkdir(parents=True)
            (path / 'lesson.json').write_text('{"kind":"guide","title":"Broken"}')
            (path / 'lesson.md').write_text('## Cíl\nJen nadpis.\n')
            before = len(validator.errors)
            validator.validate_lesson(Path(work), path.name, Path(work))
            found = validator.errors[before:]
            del validator.errors[before:]
            self.assertTrue(any('Praktický krok' in e for e in found))
            self.assertTrue(any('kontrolní seznam' in e for e in found))

    def test_http_profiles_and_documents(self):
        server = create_server(ROOT, '127.0.0.1', 0)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            def get(path):
                conn = http.client.HTTPConnection(*server.server_address, timeout=10)
                try:
                    conn.request('GET', path)
                    response = conn.getresponse()
                    return response.status, json.loads(response.read())
                finally:
                    conn.close()
            for cid in PROFILES:
                status, body = get('/api/preparation?course=' + cid)
                self.assertEqual(status, 200)
                self.assertEqual(body['course'], cid)
            for cid in ['unknown', '../zaklady', '']:
                self.assertEqual(get('/api/preparation?course=' + cid)[0], 404)
            for doc in ['vscode', 'vscodium', 'pycharm']:
                self.assertEqual(get('/api/doc?name=' + doc)[0], 200)
            self.assertEqual(get('/api/doc?name=../app')[0], 404)
        finally:
            server.runs.stop_all()
            server.shutdown()
            server.server_close()


if __name__ == '__main__':
    unittest.main()
