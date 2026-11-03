"""Testy pomocných nástrojů: setup_env, install_extensions, výběr Pythonu z .venv, /api/doc."""
import http.client, json, subprocess, sys, tempfile, threading, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import setup_env  # noqa: E402
from server.app import create_server  # noqa: E402


class ToolsTest(unittest.TestCase):
    def test_packages_per_course(self):
        self.assertEqual(setup_env.wanted("zaklady"), [])
        self.assertIn("pygame-ce", setup_env.wanted("pygame-1"))
        self.assertNotIn("pygame", setup_env.wanted("all"))
        self.assertEqual(len(setup_env.wanted("pygame-1,pygame-2")), 1, "bez duplicit")
        with self.assertRaises(SystemExit):
            setup_env.wanted("neexistuje")

    def test_all_catalog_courses_have_packages_entry(self):
        cat = json.loads((ROOT / "courses" / "catalog.json").read_text("utf-8"))["courses"]
        self.assertEqual({c["id"] for c in cat}, set(setup_env.PACKAGES))

    def test_dry_run(self):
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "setup_env.py"), "--dry-run"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0); self.assertIn("pandas", r.stdout)

    def test_venv_created_without_install(self):
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(ROOT / "tools" / "setup_env.py"), "--venv", str(Path(d) / "v"), "--no-install"],
                               capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((Path(d) / "v" / "pyvenv.cfg").is_file())

    def test_extensions_dry_run_matches_json(self):
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "install_extensions.py"), "--dry-run"], capture_output=True, text=True)
        want = json.loads((ROOT / ".vscode" / "extensions.json").read_text("utf-8"))["recommendations"]
        self.assertEqual(r.returncode, 0)
        for e in want: self.assertIn(e, r.stdout)

    def test_vscode_json_valid_and_no_pylance(self):
        for f in ("extensions.json", "settings.json", "tasks.json", "launch.json"):
            json.loads((ROOT / ".vscode" / f).read_text("utf-8"))
        ext = json.loads((ROOT / ".vscode" / "extensions.json").read_text("utf-8"))
        self.assertNotIn("ms-python.vscode-pylance", ext["recommendations"])
        json.loads((ROOT / "pyrightconfig.json").read_text("utf-8"))

    def test_doc_api(self):
        srv = create_server(ROOT, "127.0.0.1", 0)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        port = srv.server_address[1]
        def get(path):
            c = http.client.HTTPConnection("127.0.0.1", port); c.request("GET", path, headers={"Host": f"127.0.0.1:{port}"})
            r = c.getresponse(); return r.status, json.loads(r.read())
        st, d = get("/api/doc?name=vscodium"); self.assertEqual(st, 200); self.assertIn("Pylance", d["md"])
        self.assertEqual(get("/api/doc?name=../server/app")[0], 404)
        srv.shutdown(); srv.server_close()

    def test_start_uses_venv_python_when_present(self):
        import start
        self.assertTrue(str(start.venv_python(Path("/x"))).replace("\\", "/").endswith(("/.venv/bin/python", "/.venv/Scripts/python.exe")))


if __name__ == "__main__":
    unittest.main()
