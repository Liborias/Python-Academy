"""Validátor obsahu musí umět selhat: rozbité lekce se musí odhalit."""
import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "courses" / "zaklady"


def run_validator(courses_dir):
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "validate_courses.py"), "--courses-dir", str(courses_dir)],
                       capture_output=True, text=True, timeout=420)
    return r.returncode, r.stdout


class ValidateTest(unittest.TestCase):
    def make(self, mutate):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        cat = json.loads((ROOT / "courses" / "catalog.json").read_text("utf-8"))
        cat["courses"] = [c for c in cat["courses"] if c["id"] == "zaklady"]
        (root / "catalog.json").write_text(json.dumps(cat), encoding="utf-8")
        shutil.copytree(SRC, root / "zaklady")
        mutate(root / "zaklady" / "lessons" / "01-prvni-program")
        return root

    def test_real_content_ok(self):
        code, out = run_validator(ROOT / "courses"); self.assertEqual(code, 0, out)

    def test_bad_solution_detected(self):
        root = self.make(lambda d: (d / "solution.py").write_text('print("jinak")\n', encoding="utf-8"))
        code, out = run_validator(root); self.assertEqual(code, 1); self.assertIn("VZOROVÉ ŘEŠENÍ NEPROŠLO", out)

    def test_starter_that_passes_detected(self):
        root = self.make(lambda d: (d / "exercise.py").write_text((d / "solution.py").read_text("utf-8"), encoding="utf-8"))
        code, out = run_validator(root); self.assertEqual(code, 1); self.assertIn("VÝCHOZÍ ŠABLONA PROŠLA", out)

    def test_missing_file_detected(self):
        root = self.make(lambda d: (d / "check.py").unlink())
        code, out = run_validator(root); self.assertEqual(code, 1); self.assertIn("chybí check.py", out)

    def test_banned_topic_detected(self):
        root = self.make(lambda d: (d / "lesson.md").write_text("## Harry Potter\nText\n", encoding="utf-8"))
        code, out = run_validator(root); self.assertEqual(code, 1); self.assertIn("zakázané téma", out)

    def test_broken_quiz_and_example_detected(self):
        def m(d):
            (d / "quiz.json").write_text('[{"q":"a","options":["x","y"],"answer":5,"why":"w"}]', encoding="utf-8")
            (d / "example.py").write_text("# a\n# b\nprint(1/0)\n", encoding="utf-8")
        code, out = run_validator(self.make(m)); self.assertEqual(code, 1)
        self.assertIn("answer mimo rozsah", out); self.assertIn("example.py skončil chybou", out)

    def test_few_comments_detected(self):
        root = self.make(lambda d: (d / "example.py").write_text('print("a")\n', encoding="utf-8"))
        code, out = run_validator(root); self.assertEqual(code, 1); self.assertIn("málo vysvětlujících komentářů", out)


if __name__ == "__main__":
    unittest.main()
