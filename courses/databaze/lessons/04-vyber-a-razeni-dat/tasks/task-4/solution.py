# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from schema import vytvor_pomucky, vytvor_kategorie, vytvor_udalosti
from podklady import priprav_sklad, vyzaduj_transakce, kladny_pocet

def prehled_jako_slovniky(con):
    kurzor = con.cursor()
    kurzor.row_factory = sqlite3.Row
    return [dict(radek) for radek in kurzor.execute('SELECT id, nazev, kusy FROM pomucky ORDER BY id')]

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        priprav_sklad(con)
        print(prehled_jako_slovniky(con))
        print('Nastavení spojení:', con.row_factory)
