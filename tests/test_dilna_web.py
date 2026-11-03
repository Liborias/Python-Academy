"""Pomocný místní server dilna_web: kopie v lekcích musí být shodné s originálem a server musí fungovat."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "courses/soubory-web/shared/dilna_web.py"


class DilnaWebTest(unittest.TestCase):
    def test_kopie_v_lekcich_jsou_shodne(self):
        kopie = list((ROOT / "courses/soubory-web/lessons").glob("*/files/dilna_web.py"))
        self.assertGreaterEqual(len(kopie), 4)
        for k in kopie:
            self.assertEqual(k.read_bytes(), SHARED.read_bytes(), f"{k} se liší od shared/dilna_web.py")

    def test_server_odpovida(self):
        import requests
        tmp = Path(tempfile.mkdtemp())
        (tmp / "web").mkdir()
        (tmp / "web" / "a.txt").write_text("ahoj", encoding="utf-8")
        sys.path.insert(0, str(SHARED.parent))
        try:
            import dilna_web
            adresa = dilna_web.spust(str(tmp / "web"))
        finally:
            sys.path.pop(0)
        self.assertTrue(adresa.startswith("http://127.0.0.1:"))
        self.assertEqual(requests.get(adresa + "/a.txt", timeout=3).text, "ahoj")
        self.assertEqual(requests.get(adresa + "/_status/418", timeout=3).status_code, 418)
        self.assertEqual(requests.get(adresa + "/nic", timeout=3).status_code, 404)
        self.assertEqual([requests.get(adresa + "/_nestabilni/x", timeout=3).status_code for _ in range(3)], [500, 500, 200])

    def test_server_neni_dostupny_zvenku(self):
        src = SHARED.read_text(encoding="utf-8")
        self.assertIn('("127.0.0.1", 0)', src)


if __name__ == "__main__":
    unittest.main()
