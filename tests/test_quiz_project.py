"""Projekt kvízu: hranice modelu, dat, přenosu a interaktivní aplikace."""
import json
import sys
import tempfile
import threading
import unittest
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.checker import run_check

BASE = ROOT/'courses/turtle-oop/lessons'
IDS = ['37-kviz-otazka-a-skore', '38-kviz-data-json', '39-kviz-api-a-zaloha', '40-kviz-hotova-aplikace']


class QuizProjectTest(unittest.TestCase):
    def source(self, index):
        return (BASE/IDS[index]/'solution.py').read_text('utf-8')

    def verify(self, index, code, expected):
        with tempfile.TemporaryDirectory() as temp:
            result = run_check(BASE/IDS[index], code, ROOT/'lib', Path(temp))
        self.assertNotIn('error', result, result)
        self.assertEqual(result.get('ok'), expected, result)

    def variants(self, index, wrong, correct):
        source = self.source(index)
        for expected, variants in [(False, wrong), (True, correct)]:
            for code in variants:
                self.assertNotEqual(code, source)
                with self.subTest(expected=expected, code=code):
                    self.verify(index, code, expected)

    def test_model(self):
        s = self.source(0)
        wrong = [
            s.replace('list(otazky)', 'otazky'),
            s.replace('self.index >= len(self.otazky)', 'self.index > len(self.otazky)'),
            s.replace('if not isinstance(odpoved, bool):', 'if False:'),
            s.replace('self.skore += 1', 'self.skore += 2'),
            s.replace('spravne = odpoved == otazka.spravne', 'spravne = bool(odpoved)'),
            s.replace('        self.index += 1', '            self.index += 1'),
            s.replace('raise ValueError("Kvíz už skončil")', 'return False'),
            s.replace('self.index', 'Kviz.index'),
        ]
        correct = [
            s.replace('list(otazky)', 'otazky[:]'),
            s.replace('not isinstance(odpoved, bool)', 'type(odpoved) is not bool')
             .replace('odpoved == otazka.spravne', 'odpoved is otazka.spravne'),
        ]
        self.variants(0, wrong, correct)

    def test_data(self):
        s = self.source(1)
        wrong = [
            s.replace('odpoved == "True"', 'bool(odpoved)'),
            s.replace('unescape(text).strip()', 'text.strip()'),
            s.replace('unescape(text).strip()', 'unescape(text)'),
            s.replace('data["response_code"] != 0', 'False'),
            s.replace('type(data.get("response_code")) is not int or ', ''),
            s.replace('return otazky', 'return list(reversed(otazky))'),
            s.replace('Path(cesta)', 'Path("otazky.json")'),
            s.replace('read_text(encoding="utf-8")', 'read_text()'),
            s.replace('raise ValueError("Neplatný text nebo odpověď")', 'continue'),
        ]
        correct = [
            s.replace('''    text = Path(cesta).read_text(encoding="utf-8")
    return preved_otazky(json.loads(text))''', '''    with open(cesta, encoding="utf-8") as soubor:
        return preved_otazky(json.load(soubor))'''),
            s.replace('otazky.append(Otazka(text, odpoved == "True"))', 'otazky += [Otazka(text, odpoved == "True")]'),
        ]
        self.variants(1, wrong, correct)

    def test_api_and_fallback(self):
        s = self.source(2)
        wrong = [
            s.replace('timeout=5', 'timeout=20'),
            s.replace('odpoved.read(MAX_BAJTU + 1)', 'odpoved.read()'),
            s.replace('odpoved.read(MAX_BAJTU + 1)', 'odpoved.read(MAX_BAJTU)'),
            s.replace('obsah.decode("utf-8")', 'obsah.decode("latin-1")'),
            s.replace('''    with urlopen(url, timeout=5) as odpoved:
        obsah = odpoved.read(MAX_BAJTU + 1)''', '''    odpoved = urlopen(url, timeout=5)
    obsah = odpoved.read(MAX_BAJTU + 1)'''),
            s.replace('if not online:', 'if False:'),
            s.replace('except (OSError, ValueError) as chyba:', 'except OSError as chyba:'),
            s.replace('except (OSError, ValueError) as chyba:', 'except Exception as chyba:'),
            s.replace('nacti_soubor(cesta)', 'nacti_soubor("otazky.json")'),
            s.replace('"záloha", f"API nelze použít: {chyba}"', '"API", ""'),
        ]
        correct = [
            s.replace('from urllib.request import urlopen', 'import urllib.request')
             .replace('with urlopen(', 'with urllib.request.urlopen('),
            s.replace('''    with urlopen(url, timeout=5) as odpoved:
        obsah = odpoved.read(MAX_BAJTU + 1)''', '''    odpoved = urlopen(url, timeout=5)
    try:
        obsah = odpoved.read(MAX_BAJTU + 1)
    finally:
        odpoved.close()'''),
        ]
        self.variants(2, wrong, correct)

    def test_interactive_quiz(self):
        s = self.source(3)
        wrong = [
            s.replace('.strip().casefold()', ''),
            s.replace('kviz.odpovez(volba == "a")', 'kviz.odpovez(bool(volba))'),
            s.replace('            break\n', '            continue\n'),
            s.replace('except EOFError:', 'except ValueError:'),
            s.replace('return kviz.skore, kviz.index', 'return kviz.skore, kviz.skore'),
            s.replace('vypis(', 'print('),
            s.replace('kviz = Kviz(otazky)', 'kviz = Kviz(otazky)\n    otazky.clear()'),
            s.replace('''            if volba == "q":
                vypis''', '''            if volba == "q":
                kviz.odpovez(False)
                vypis'''),
        ]
        correct = [
            s.replace('.casefold()', '.lower()'),
            s.replace('while kviz.aktualni() is not None:', 'while kviz.index < len(kviz.otazky):'),
        ]
        self.variants(3, wrong, correct)

    def test_modules_and_original_offline_data(self):
        modules = [('kviz_model.py', IDS[0]), ('kviz_data.py', IDS[1]), ('kviz_api.py', IDS[2])]
        for index in range(1, 4):
            for filename, previous in modules[:index]:
                self.assertEqual((BASE/IDS[index]/'files'/filename).read_text('utf-8'), (BASE/previous/'solution.py').read_text('utf-8'))
            self.assertEqual((BASE/IDS[index]/'files/otazky.json').read_bytes(), (ROOT/'courses/turtle-oop/data/kviz-otazky.json').read_bytes())
        self.assertEqual((BASE/IDS[2]/'files/api_ukazka.json').read_bytes(), (ROOT/'courses/turtle-oop/data/kviz-api-ukazka.json').read_bytes())

    def test_http_transport_on_local_server(self):
        payload = {'response_code': 0, 'results': [{'type': 'boolean', 'question': 'Řeka &amp; les', 'correct_answer': 'True'}]}
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass
            def do_GET(self):
                requests.append(self.path)
                status = 503 if self.path == '/error' else 200
                body = {'/ok': json.dumps(payload, ensure_ascii=False).encode('utf-8'), '/invalid': b'{JSON',
                        '/large': b'{}' + b' ' * 65_535, '/utf8': b'\xff', '/error': b''}[self.path]
                self.send_response(status)
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        names = ['kviz_model', 'kviz_data']
        previous = {name: sys.modules.get(name) for name in names}
        sys.path.insert(0, str(BASE/IDS[2]/'files'))
        for name in names:
            sys.modules.pop(name, None)
        try:
            path = BASE/IDS[2]/'solution.py'
            ns = {'__name__': 'quiz_transport_test', '__file__': str(path)}
            exec(compile(path.read_text('utf-8'), str(path), 'exec'), ns)
            # Pouze loopback test má vlastní přímý opener; síťová konfigurace aplikace zůstává zděděná.
            ns['urlopen'] = urllib.request.build_opener(urllib.request.ProxyHandler({})).open
            base = f'http://127.0.0.1:{server.server_address[1]}'
            self.assertEqual(ns['stahni_json'](base+'/ok'), payload)
            for route, error in [('/invalid', ValueError), ('/large', ValueError), ('/utf8', ValueError), ('/error', OSError)]:
                with self.subTest(route=route), self.assertRaises(error):
                    ns['stahni_json'](base+route)
            self.assertEqual(requests, ['/ok', '/invalid', '/large', '/utf8', '/error'])
        finally:
            sys.path.pop(0)
            for name, module in previous.items():
                if module is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = module
            server.shutdown()
            server.server_close()


if __name__ == '__main__':
    unittest.main()
