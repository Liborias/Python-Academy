import json
from pathlib import Path
import queue
import smtplib
import tempfile
import unittest
from unittest.mock import patch
import dilna
import prenos
import priprava
from zpravy import vytvor_zpravu


# Každý test používá vlastní dočasnou složku nebo frontu, žádnou osobní schránku.
class TestDilna(unittest.TestCase):
    def test_neuplny_koncept_se_zachova(self):
        with tempfile.TemporaryDirectory() as folder:
            cesta = Path(folder) / "koncept.json"
            model = {"prijemce": "jan@", "predmet": "  Žofie  ", "text": " A\nB\n",
                     "priloha": str(Path(folder) / "chybi.txt")}
            puvodni = dict(model)
            dilna.uloz_koncept(cesta, model)
            self.assertEqual(dilna.nacti_koncept(cesta), model)
            self.assertEqual(model, puvodni)

    def test_chybna_verze_a_typ(self):
        with tempfile.TemporaryDirectory() as folder:
            cesta = Path(folder) / "chyba.json"
            model = dict.fromkeys(("prijemce", "predmet", "text", "priloha"), "")
            for dokument in [{"verze": True, "koncept": model}, {"verze": 2, "koncept": model},
                             {"verze": 1, "koncept": dict(model, text=3)}]:
                with self.subTest(dokument=dokument):
                    cesta.write_text(json.dumps(dokument), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        dilna.nacti_koncept(cesta)

    def test_chyba_zapisu_zachova_starsi_praci(self):
        with tempfile.TemporaryDirectory() as folder:
            cesta = Path(folder) / "koncept.json"
            cesta.write_text("Původní práce", encoding="utf-8")
            model = dict.fromkeys(("prijemce", "predmet", "text", "priloha"), "")
            # Selhání nahrazení vyvoláme řízeně, stav disku potom skutečně přečteme.
            with patch("dilna.os.replace", side_effect=OSError("Cvičná chyba")):
                with self.assertRaises(OSError):
                    dilna.uloz_koncept(cesta, model)
            self.assertEqual(cesta.read_text(encoding="utf-8"), "Původní práce")
            self.assertEqual(list(Path(folder).glob(".koncept-*.tmp")), [])

    def test_pracovnik_predava_stavy_a_argumenty(self):
        zprava = vytvor_zpravu("eva@example.test", "jan@example.test", "Test", "České tělo")
        scenare = [(None, "prijato"), (smtplib.SMTPRecipientsRefused({"jan@example.test": (550, b"no")}), "odmitnuto"),
                   (smtplib.SMTPServerDisconnected("Cvičné čekání"), "nejiste")]
        for chyba, stav in scenare:
            with self.subTest(stav=stav):
                fronta = queue.Queue()
                with patch("prenos.odesli_do_zachytu", side_effect=chyba) as odesli:
                    prenos.predat_zpravu(zprava, "127.0.0.1", 43210, 0.2, fronta)
                odesli.assert_called_once_with(zprava, "127.0.0.1", 43210, 0.2)
                self.assertEqual(fronta.get_nowait(), stav)
                self.assertTrue(fronta.empty())

    def test_zprava_je_samostatny_snimek(self):
        with tempfile.TemporaryDirectory() as folder:
            cesta = Path(folder) / "česká příloha.txt"
            data = "Žofie\n".encode("utf-8")
            cesta.write_bytes(data)
            model = {"prijemce": "jan@example.test", "predmet": "Původní předmět",
                     "text": " A\nB\n", "priloha": str(cesta)}
            zprava = priprava.sestav_zpravu(model)
            model["predmet"] = "Později"
            cesta.write_bytes(b"jine bajty")
            self.assertEqual(str(zprava["Subject"]), "Původní předmět")
            self.assertEqual(zprava.get_body(preferencelist=("plain",)).get_content(), " A\nB\n")
            self.assertEqual(list(zprava.iter_attachments())[0].get_payload(decode=True), data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
