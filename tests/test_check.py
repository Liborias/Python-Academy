"""Testy knihovny dilna_check a /api/check."""
import http.client, json, sys, threading, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server  # noqa: E402

GOOD1 = 'jmeno = input("Jméno: ")\nprint("Ahoj", jmeno)\n'
GOOD2 = 'def secti(a, b):\n    return a + b\n\nif __name__ == "__main__":\n    print(secti(1, 2))\n'


class CheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = create_server(ROOT, "127.0.0.1", 0, courses_dir=ROOT / "tests" / "fixtures")
        cls.port = cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown(); cls.srv.server_close()

    def chk(self, lesson, code, course="demo", token=True):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=30)
        h = {"Host": f"127.0.0.1:{self.port}", "Content-Type": "application/json"}
        if token:
            h["X-Dilna-Token"] = self.srv.token
        c.request("POST", "/api/check", json.dumps({"course": course, "lesson": lesson, "code": code}), h)
        r = c.getresponse()
        return r.status, json.loads(r.read())

    def test_good_passes(self):
        st, d = self.chk("01-pozdrav", GOOD1)
        self.assertEqual(st, 200); self.assertTrue(d["ok"], d)
        st, d = self.chk("02-funkce", GOOD2)
        self.assertTrue(d["ok"], d)

    def test_main_guard_not_run_on_load(self):
        # blok __main__ se při load() nespustí, takže výstup nevadí a kontrola projde
        st, d = self.chk("02-funkce", GOOD2 + "\nwhile False: pass\n")
        self.assertTrue(d["ok"], d)

    def test_wrong_output(self):
        _, d = self.chk("01-pozdrav", 'input()\nprint("Ahoj Karle")')
        self.assertFalse(d["ok"])
        self.assertTrue(any("Ahoj Eva" in r["name"] for r in d["results"] if not r["ok"]))

    def test_wrong_function_result(self):
        _, d = self.chk("02-funkce", "def secti(a, b):\n    return a - b\n")
        self.assertFalse(d["ok"])
        self.assertIn("vrátila", " ".join(r["msg"] for r in d["results"]))

    def test_missing_function(self):
        _, d = self.chk("02-funkce", "x = 1")
        self.assertFalse(d["ok"])

    def test_syntax_error_reported(self):
        _, d = self.chk("02-funkce", "def secti(a, b:\n  return")
        self.assertFalse(d["ok"])
        self.assertTrue(any("Syntaxe" == r["name"] for r in d["results"]))

    def test_runtime_error_in_student(self):
        _, d = self.chk("01-pozdrav", "print(1/0)")
        self.assertFalse(d["ok"])
        self.assertIn("ZeroDivisionError", json.dumps(d, ensure_ascii=False))

    def test_infinite_loop_does_not_hang(self):
        _, d = self.chk("01-pozdrav", "while True: pass")
        self.assertFalse(d["ok"])

    def test_forbidden_call(self):
        _, d = self.chk("02-funkce", GOOD2 + "eval('1')\n")
        self.assertFalse(d["ok"])

    def test_requires_token(self):
        self.assertEqual(self.chk("01-pozdrav", GOOD1, token=False)[0], 401)

    def test_bad_ids(self):
        self.assertEqual(self.chk("../../server", GOOD1)[0], 404)
        self.assertEqual(self.chk("01-pozdrav", GOOD1, course="../x")[0], 404)
        self.assertEqual(self.chk("neexistuje", GOOD1)[0], 404)


class TestNoveMetody(unittest.TestCase):
    def test_raises_a_close(self):
        import os, tempfile
        sys.path.insert(0, str(ROOT / "lib"))
        from dilna_check import Checker
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "reseni.py"
            src.write_text("def f(x):\n    raise ValueError('x')\ndef g():\n    return 1.0000000001\n", encoding="utf-8")
            os.environ["DILNA_STUDENT"] = str(src)
            os.environ["DILNA_RESULT"] = str(Path(d) / "r.json")
            c = Checker()
            ns = c.load()
            self.assertTrue(c.raises(ns, "f", (1,), ValueError))
            self.assertFalse(c.raises(ns, "f", (1,), KeyError))
            self.assertTrue(c.returns_close(ns, "g", (), 1.0))
            self.assertFalse(c.returns_close(ns, "g", (), 2.0))

if __name__ == "__main__":
    unittest.main()
