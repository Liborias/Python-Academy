"""Pomocné soubory lekce (files/) při spuštění, kontrole a ukládání do pracovní složky."""
import http.client, json, sys, tempfile, threading, time, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server.app import create_server  # noqa: E402
from server.lessonfiles import copy_files  # noqa: E402

CODE = 'with open("data.txt", encoding="utf-8") as f:\n    print(len(f.readlines()))\n'


class FilesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = create_server(ROOT, "127.0.0.1", 0, courses_dir=ROOT / "tests" / "fixtures")
        cls.port = cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown(); cls.srv.server_close()

    def post(self, path, body):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=30)
        h = {"Host": f"127.0.0.1:{self.port}", "Content-Type": "application/json", "X-Dilna-Token": self.srv.token}
        c.request("POST", path, json.dumps(body), h)
        r = c.getresponse()
        return r.status, json.loads(r.read())

    def poll(self, rid):
        for _ in range(100):
            c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=30)
            c.request("GET", f"/api/run/poll?id={rid}&since=0", headers={
                "Host": f"127.0.0.1:{self.port}", "X-Dilna-Token": self.srv.token})
            d = json.loads(c.getresponse().read())
            if d["done"]:
                return d
            time.sleep(0.1)
        self.fail("běh neskončil")

    def test_run_sees_lesson_files(self):
        st, d = self.post("/api/run", {"code": CODE, "course": "demo", "lesson": "03-soubor"})
        self.assertEqual(st, 200)
        p = self.poll(d["id"])
        self.assertEqual(p["exit"], 0)
        self.assertIn("2", "".join(c["text"] for c in p["chunks"]))

    def test_run_without_lesson_has_no_files(self):
        _, d = self.post("/api/run", {"code": CODE})
        p = self.poll(d["id"])
        self.assertNotEqual(p["exit"], 0)

    def test_check_sees_lesson_files(self):
        _, d = self.post("/api/check", {"course": "demo", "lesson": "03-soubor", "code": CODE})
        self.assertTrue(d["ok"], d)

    def test_bad_lesson_id_ignored(self):
        _, d = self.post("/api/run", {"code": "print(1)", "course": "../demo", "lesson": "03-soubor"})
        self.assertEqual(self.poll(d["id"])["exit"], 0)

    def test_copy_files_skips_symlinks_and_keeps_existing(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            a, b = Path(a), Path(b)
            (a / "x.txt").write_text("1"); (a / "sub").mkdir(); (a / "sub" / "y.txt").write_text("2")
            try:
                (a / "link").symlink_to("/etc/hostname")
            except OSError:
                pass
            (b / "x.txt").write_text("moje")
            copy_files(a, b, overwrite=False)
            self.assertEqual((b / "x.txt").read_text(), "moje")
            self.assertEqual((b / "sub" / "y.txt").read_text(), "2")
            self.assertFalse((b / "link").exists())

    def test_workspace_gets_files(self):
        _, d = self.post("/api/workspace/save", {"course": "demo", "lesson": "03-soubor", "code": CODE})
        folder = Path(d["path"]).parent
        self.assertTrue((folder / "data.txt").is_file())


if __name__ == "__main__":
    unittest.main()
