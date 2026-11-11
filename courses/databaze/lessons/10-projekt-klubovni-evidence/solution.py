# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from relacni_schema import spojeni_s_vazbami, vytvor_relacni_schema
from operace import zapis_pomucku
from dotazy import vsechny_pomucky
from pomoc import cisty_nazev, nezaporny_pocet, zkontroluj_schema
from ukazka import ukazka

class Evidence:
    def __init__(self, cesta):
        self.con = spojeni_s_vazbami(cesta)
        try:
            with self.con:
                vytvor_relacni_schema(self.con)
                zkontroluj_schema(self.con)
        except Exception:
            self.con.close()
            raise

    def close(self):
        self.con.close()

    def pridej_kategorii(self, nazev):
        nazev = cisty_nazev(nazev)
        with self.con:
            return self.con.execute('INSERT INTO kategorie (nazev) VALUES (?)', (nazev,)).lastrowid

    def pridej_pomucku(self, nazev, kusy, kategorie_id=None):
        nazev = cisty_nazev(nazev)
        nezaporny_pocet(kusy)
        with self.con:
            return zapis_pomucku(self.con, nazev, kusy, kategorie_id)

    def prehled(self):
        with self.con:
            return vsechny_pomucky(self.con)

    def pujc(self, pomucka_id, clen):
        clen = cisty_nazev(clen)
        with self.con:
            kurzor = self.con.execute('UPDATE pomucky SET kusy = kusy - 1 WHERE id = ? AND kusy > 0', (pomucka_id,))
            if kurzor.rowcount != 1:
                raise ValueError('Pomůcka není dostupná.')
            return self.con.execute('INSERT INTO vypujcky (pomucka_id, clen) VALUES (?, ?)',
                                    (pomucka_id, clen)).lastrowid

    def vrat(self, vypujcka_id):
        with self.con:
            radek = self.con.execute('SELECT pomucka_id FROM vypujcky WHERE id = ? AND vraceno = 0',
                                     (vypujcka_id,)).fetchone()
            if radek is None:
                return False
            self.con.execute('UPDATE pomucky SET kusy = kusy + 1 WHERE id = ?', (radek[0],))
            self.con.execute('UPDATE vypujcky SET vraceno = 1 WHERE id = ?', (vypujcka_id,))
            return True

    def aktivni_vypujcky(self):
        with self.con:
            return self.con.execute('''
                SELECT v.id, p.nazev, v.clen FROM vypujcky AS v
                JOIN pomucky AS p ON p.id = v.pomucka_id
                WHERE v.vraceno = 0 ORDER BY v.id
            ''').fetchall()

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    ukazka(Evidence)
