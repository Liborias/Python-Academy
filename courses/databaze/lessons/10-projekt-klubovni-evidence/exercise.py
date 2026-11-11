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
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def pridej_kategorii(self, nazev):
        raise NotImplementedError

    def pridej_pomucku(self, nazev, kusy, kategorie_id=None):
        raise NotImplementedError

    def prehled(self):
        raise NotImplementedError

    def pujc(self, pomucka_id, clen):
        raise NotImplementedError

    def vrat(self, vypujcka_id):
        raise NotImplementedError

    def aktivni_vypujcky(self):
        raise NotImplementedError

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    ukazka(Evidence)
