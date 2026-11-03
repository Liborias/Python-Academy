"""Spustitelný příklad nové lekce: token, pevný program a interpreter .venv."""
import http.client
import importlib.util
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ROOT / 'courses/priprava/lessons/09-server-a-token/files'
spec = importlib.util.spec_from_file_location('lesson_token_server', FILES / 'token_server.py')
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class TokenLessonTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_root = demo.ROOT
        demo.ROOT = Path(self.temp.name)
        # Výpis je z přiloženého programu. Značka odhalí i nechtěný běh.
        (demo.ROOT / 'main.py').write_text(
            (FILES / 'main.py').read_text('utf-8') +
            '\nfrom pathlib import Path\nPath("executed").write_text("yes")\n', encoding='utf-8')
        self.server = demo.create_server(0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
        demo.ROOT = self.old_root
        self.temp.cleanup()

    def request(self, token=None, method='POST', path='/run', body=b'', headers=None):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=10)
        values = dict(headers or {})
        if token is not None:
            values['X-Project-Token'] = token
        try:
            connection.request(method, path, body=body, headers=values)
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()

    def test_valid_token_runs_fixed_file_with_same_python(self):
        status, result = self.request(self.server.token)
        self.assertEqual(status, 200)
        self.assertEqual(result['exit'], 0)
        self.assertIn(sys.executable, result['stdout'])
        self.assertIn('Ahoj z projektu', result['stdout'])
        self.assertIn('Virtuální prostředí: ' + str(sys.prefix != sys.base_prefix), result['stdout'])
        self.assertTrue((demo.ROOT / 'executed').is_file())

    def test_wrong_and_missing_token_do_not_run_program(self):
        for token in [None, 'invalid', '']:
            self.assertEqual(self.request(token)[0], 401)
        self.assertFalse((demo.ROOT / 'executed').exists())

    def test_restart_issues_a_new_token(self):
        other = demo.create_server(0)
        try:
            self.assertNotEqual(other.token, self.server.token)
            self.assertEqual(self.request(other.token)[0], 401)
        finally:
            other.server_close()
        self.assertFalse((demo.ROOT / 'executed').exists())

    def test_no_client_code_paths_or_shell_commands(self):
        for body in [b'{"code":"print(1)"}', b'{"path":"other.py"}']:
            self.assertEqual(self.request(self.server.token, body=body)[0], 400)
        self.assertEqual(self.request(self.server.token, path='/other.py')[0], 404)
        self.assertEqual(self.request(self.server.token, path='/run?token=value')[0], 404)
        self.assertFalse((demo.ROOT / 'executed').exists())

    def test_get_and_foreign_origins_do_not_run_program(self):
        self.assertEqual(self.request(self.server.token, method='GET')[0], 405)
        self.assertEqual(self.request(self.server.token, headers={'Origin': 'http://example.invalid'})[0], 403)
        self.assertEqual(self.request(self.server.token, headers={'Host': 'example.invalid'})[0], 403)
        self.assertFalse((demo.ROOT / 'executed').exists())

    def test_program_failure_is_reported(self):
        (demo.ROOT / 'main.py').write_text('raise ValueError("ukazkova chyba")\n')
        status, result = self.request(self.server.token)
        self.assertEqual(status, 500)
        self.assertNotEqual(result['exit'], 0)
        self.assertIn('ukazkova chyba', result['stderr'])


if __name__ == '__main__':
    unittest.main()
