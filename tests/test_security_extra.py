"""Další bezpečnostní testy serveru: statické soubory, cesty, CORS, souběh, workspace."""
import http.client, json, sys, threading, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server  # noqa: E402


class SecTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = create_server(ROOT, "127.0.0.1", 0)
        cls.port = cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.runs.stop_all(); cls.srv.shutdown(); cls.srv.server_close()

    def req(self, method, path, body=None, token=True, headers=None):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        h = {"Host": f"127.0.0.1:{self.port}"}
        if token: h["X-Dilna-Token"] = self.srv.token
        h.update(headers or {})
        c.request(method, path, body=json.dumps(body) if body is not None else None, headers=h)
        r = c.getresponse(); raw = r.read()
        return r, raw

    def test_static_cannot_reach_project_files(self):
        for p in ("/../server/app.py", "/%2e%2e/server/app.py", "/..%2fserver%2fapp.py", "/server/app.py", "/courses/catalog.json",
                  "/../lib/dilna_check/__init__.py", "/%2e%2e/%2e%2e/etc/passwd", "/workspace/_run"):
            r, raw = self.req("GET", p, token=False)
            self.assertNotEqual(r.status, 200, p)
            self.assertNotIn(b"hmac", raw); self.assertNotIn(b"root:", raw)

    def test_token_never_in_static_or_api_output(self):
        for p in ("/", "/js/app.js", "/api/catalog"):
            r, raw = self.req("GET", p, token=False)
            self.assertNotIn(self.srv.token.encode(), raw, p)

    def test_no_cors_headers(self):
        r, _ = self.req("GET", "/api/catalog", token=False, headers={"Origin": f"http://127.0.0.1:{self.port}"})
        self.assertIsNone(r.getheader("Access-Control-Allow-Origin"))
        self.assertEqual(r.getheader("X-Content-Type-Options"), "nosniff")

    def test_options_preflight_not_allowed(self):
        r, _ = self.req("OPTIONS", "/api/run", token=False, headers={"Origin": "http://evil.example", "Access-Control-Request-Method": "POST"})
        self.assertNotEqual(r.status, 200)
        self.assertIsNone(r.getheader("Access-Control-Allow-Origin"))

    def test_text_plain_cross_origin_simple_request_blocked(self):
        # „jednoduchý“ POST z cizí stránky (text/plain) nesmí spustit kód: chybí token i Origin nesedí
        r, _ = self.req("POST", "/api/run", {"code": "print(1)"}, token=False,
                        headers={"Origin": "http://evil.example", "Content-Type": "text/plain"})
        self.assertIn(r.status, (401, 403))

    def test_workspace_ids_validated(self):
        for cid, lid in (("../x", "a"), ("a", "../../etc"), ("a/b", "c"), ("", "a"), ("A", "b")):
            r, _ = self.req("POST", "/api/workspace/save", {"course": cid, "lesson": lid, "code": "x"})
            self.assertEqual(r.status, 400, (cid, lid))
            r, _ = self.req("GET", f"/api/workspace?course={cid}&lesson={lid}")
            self.assertEqual(r.status, 404, (cid, lid))
        self.assertFalse((ROOT / "workspace" / "x").exists())

    def test_workspace_requires_token(self):
        r, _ = self.req("GET", "/api/workspace?course=zaklady&lesson=01-prvni-program", token=False)
        self.assertEqual(r.status, 401)

    def test_concurrency_limit(self):
        ids, last = [], None
        for _ in range(6):
            r, raw = self.req("POST", "/api/run", {"code": "import time; time.sleep(30)", "timeout": 30})
            last = r.status
            if r.status == 200: ids.append(json.loads(raw)["id"])
        self.assertEqual(len(ids), 4); self.assertEqual(last, 429)
        for i in ids: self.req("POST", "/api/run/stop", {"id": i})

    def test_traceback_hides_temp_path(self):
        import time
        for _ in range(10):                       # předchozí testy mohou ještě držet limit souběžných běhů (429)
            r, raw = self.req("POST", "/api/run", {"code": "1/0"})
            if "id" in json.loads(raw):
                break
            time.sleep(0.5)
        rid = json.loads(raw)["id"]
        time.sleep(1.2)
        _, raw = self.req("GET", f"/api/run/poll?id={rid}&since=0")
        text = "".join(c["text"] for c in json.loads(raw)["chunks"])
        self.assertIn("ZeroDivisionError", text); self.assertNotIn("run-", text); self.assertIn('File "main.py"', text)


if __name__ == "__main__":
    unittest.main()
