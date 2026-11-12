# Každý test má vlastní dočasný soubor a zavře model před úklidem.
import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import closing
from model import Pujcovna
from luhn import kontrolni_cislice

def vytvor_sadu(Pujcovna):
    class TestPujcovny(unittest.TestCase):
        def setUp(self):
            self.tmp = TemporaryDirectory()
            self.addCleanup(self.tmp.cleanup)
            self.cesta = Path(self.tmp.name)/'zkouska.sqlite3'
            self.model = Pujcovna(self.cesta)
            self.addCleanup(self.model.close)

        def test_ulozeni_a_presny_nazev(self):
            ident = self.model.pridej_pomucku("  Karty O'Neil  ",2)
            self.model.close()
            with closing(Pujcovna(self.cesta)) as znovu:
                self.assertEqual(znovu.prehled(),[(ident,"Karty O'Neil",2,None)])

        def test_kod_a_poskozena_cislice(self):
            ident = self.model.pridej_pomucku('Míč',2)
            kod = self.model.kod(ident)
            self.assertEqual(self.model.id_z_kodu(kod),ident)
            self.assertEqual(kod,str(ident)+kontrolni_cislice(str(ident)))
            s_chybou = kod[:-1]+str((int(kod[-1])+1)%10)
            with self.assertRaises(ValueError):
                self.model.id_z_kodu(s_chybou)

        def test_nedostupny_kus(self):
            ident = self.model.pridej_pomucku('Míč',0)
            with self.assertRaises(ValueError):
                self.model.pujc_kod(self.model.kod(ident),'Žofie')
            self.assertEqual(self.model.prehled()[0][2],0)
            self.assertEqual(self.model.aktivni_vypujcky(),[])

        def test_vraceni_jen_jednou(self):
            ident = self.model.pridej_pomucku('Míč',1)
            vypujcka = self.model.pujc_kod(self.model.kod(ident),'Žofie')
            self.assertEqual(self.model.prehled()[0][2],0)
            self.assertTrue(self.model.vrat(vypujcka))
            self.assertFalse(self.model.vrat(vypujcka))
            self.assertEqual(self.model.prehled()[0][2],1)

        def test_kanonicky_kod_a_neexistujici_id(self):
            ident = self.model.pridej_pomucku('Míč',1)
            telo = '0'+str(ident)
            with self.assertRaises(ValueError):self.model.id_z_kodu(telo+kontrolni_cislice(telo))
            with self.assertRaises(ValueError):self.model.kod(999)
            with self.assertRaises(ValueError):self.model.id_z_kodu('999'+kontrolni_cislice('999'))

        def test_chyba_druheho_zapisu_vrati_odecet(self):
            ident = self.model.pridej_pomucku('Míč',1)
            with self.model.con:
                self.model.con.execute("CREATE TRIGGER stop BEFORE INSERT ON vypujcky BEGIN SELECT RAISE(ABORT,'zkouška'); END")
            with self.assertRaises(sqlite3.IntegrityError):self.model.pujc_kod(self.model.kod(ident),'Žofie')
            self.assertEqual(self.model.prehled()[0][2],1)
            self.assertEqual(self.model.aktivni_vypujcky(),[])
    return unittest.defaultTestLoader.loadTestsFromTestCase(TestPujcovny)

# Sestavení sady nic nespouští, úspěch programu má návratový kód 0.
if __name__ == '__main__':
    vysledek = unittest.TextTestRunner(verbosity=2).run(vytvor_sadu(Pujcovna))
    raise SystemExit(0 if vysledek.wasSuccessful() else 1)
