"""Testy serveru: spouštění kódu, vstup, časový limit, limit výstupu, bezpečnost.
Spuštění:  python -I -m unittest discover -s tests -v   (z kořene projektu)
"""
import http.client
import json
import sys
import threading
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server  # noqa: E402


class ServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = create_server(ROOT, "127.0.0.1", 0)
        cls.port = cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.runs.stop_all()
        cls.srv.shutdown()
        cls.srv.server_close()

    def req(self, method, path, body=None, token=True, host=None, origin=None):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        h = {"Host": host or f"127.0.0.1:{self.port}"}
        if token is True:
            h["X-Dilna-Token"] = self.srv.token
        elif token:
            h["X-Dilna-Token"] = token
        if origin:
            h["Origin"] = origin
        data = json.dumps(body) if body is not None else None
        if data:
            h["Content-Type"] = "application/json"
        c.request(method, path, body=data, headers=h)
        r = c.getresponse()
        raw = r.read()
        try:
            return r.status, json.loads(raw)
        except ValueError:
            return r.status, raw

    def run_code(self, code, timeout=10, stdin="", wait=15):
        st, d = self.req("POST", "/api/run", {"code": code, "timeout": timeout, "stdin": stdin})
        self.assertEqual(st, 200, d)
        rid, since, out, err = d["id"], 0, "", ""
        end = time.time() + wait
        while time.time() < end:
            _, p = self.req("GET", f"/api/run/poll?id={rid}&since={since}")
            since = p["next"]
            for c in p["chunks"]:
                if c["ch"] == "out":
                    out += c["text"]
                else:
                    err += c["text"]
            if p["done"]:
                return out, err, p
            time.sleep(0.05)
        self.fail("běh neskončil")

    # --- funkce ---
    def test_hello_utf8(self):
        out, err, p = self.run_code('print("Ahoj světe, žluťoučký kůň")')
        self.assertEqual(out.strip(), "Ahoj světe, žluťoučký kůň")
        self.assertEqual(p["exit"], 0)

    def test_stdin_prefilled(self):
        out, _, _ = self.run_code('n = input("Jméno: ")\nprint("Ahoj", n)', stdin="Eva\n")
        self.assertIn("Jméno: ", out)
        self.assertIn("Ahoj Eva", out)

    def test_interactive_input(self):
        st, d = self.req("POST", "/api/run", {"code": 'x = input("? ")\nprint("got", x)'})
        rid = d["id"]
        time.sleep(0.5)
        self.assertTrue(self.req("POST", "/api/run/input", {"id": rid, "text": "42\n"})[1]["ok"])
        out, since = "", 0
        for _ in range(100):
            _, p = self.req("GET", f"/api/run/poll?id={rid}&since={since}")
            since = p["next"]
            out += "".join(c["text"] for c in p["chunks"] if c["ch"] == "out")
            if p["done"]:
                break
            time.sleep(0.05)
        self.assertIn("got 42", out)

    def test_error_goes_to_stderr(self):
        out, err, p = self.run_code("1/0")
        self.assertIn("ZeroDivisionError", err)
        self.assertNotEqual(p["exit"], 0)

    def test_timeout(self):
        t = time.time()
        _, _, p = self.run_code("while True: pass", timeout=1)
        self.assertTrue(p["timed_out"])
        self.assertLess(time.time() - t, 6)

    def test_output_limit(self):
        _, _, p = self.run_code("while True: print('x' * 1000)", timeout=20)
        self.assertTrue(p["truncated"])

    def test_stop(self):
        st, d = self.req("POST", "/api/run", {"code": "import time\ntime.sleep(60)", "timeout": 60})
        self.req("POST", "/api/run/stop", {"id": d["id"]})
        for _ in range(60):
            _, p = self.req("GET", f"/api/run/poll?id={d['id']}&since=0")
            if p["done"]:
                break
            time.sleep(0.05)
        self.assertTrue(p["done"] and p["stopped"])

    def test_env_has_no_secrets(self):
        import os
        os.environ["DILNA_TEST_SECRET"] = "tajne"
        out, _, _ = self.run_code("import os; print(os.environ.get('DILNA_TEST_SECRET'))")
        self.assertEqual(out.strip(), "None")

    def test_temp_dir_cleaned(self):
        self.run_code("print(1)")
        time.sleep(0.5)
        left = [p for p in (ROOT / "workspace" / "_run").iterdir() if p.name.startswith("run-")]
        self.assertEqual(left, [])

    # --- bezpečnost ---
    def test_no_token(self):
        self.assertEqual(self.req("POST", "/api/run", {"code": "print(1)"}, token=False)[0], 401)
        self.assertEqual(self.req("GET", "/api/run/poll?id=x", token=False)[0], 401)

    def test_wrong_token(self):
        self.assertEqual(self.req("POST", "/api/run", {"code": "print(1)"}, token="spatny")[0], 401)

    def test_bad_host_rebinding(self):
        self.assertEqual(self.req("GET", "/api/catalog", host="evil.example:80")[0], 403)
        self.assertEqual(self.req("POST", "/api/run", {"code": "print(1)"}, host="evil.example")[0], 403)

    def test_bad_origin(self):
        self.assertEqual(self.req("POST", "/api/run", {"code": "print(1)"}, origin="http://evil.example")[0], 403)
        self.assertEqual(self.req("POST", "/api/run", {"code": "print(1)"},
                                  origin=f"http://127.0.0.1:{self.port + 1}")[0], 403)

    def test_good_origin(self):
        st, _ = self.req("GET", "/api/catalog", origin=f"http://localhost:{self.port}")
        self.assertEqual(st, 200)

    def test_oversize_and_bad_json(self):
        self.assertEqual(self.req("POST", "/api/run", {"code": "x" * 300_001})[0], 413)
        c = http.client.HTTPConnection("127.0.0.1", self.port)
        c.request("POST", "/api/run", body="{nejson", headers={
            "Host": f"127.0.0.1:{self.port}", "X-Dilna-Token": self.srv.token, "Content-Length": "7"})
        self.assertEqual(c.getresponse().status, 400)

    def test_path_traversal(self):
        c = http.client.HTTPConnection("127.0.0.1", self.port)
        c.request("GET", "/../server/security.py", headers={"Host": f"127.0.0.1:{self.port}"})
        r = c.getresponse()
        self.assertIn(r.status, (301, 400, 404))
        self.assertNotIn(b"hmac", r.read())

    def test_only_loopback(self):
        with self.assertRaises(ValueError):
            create_server(ROOT, "0.0.0.0", 0)


if __name__ == "__main__":
    unittest.main()
