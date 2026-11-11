# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from schema import vytvor_pomucky, vytvor_kategorie

def vytvor_sklad(con):
    vytvor_pomucky(con)
    vytvor_kategorie(con)

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        vytvor_sklad(con)
        vytvor_sklad(con)
        print(con.execute("SELECT name FROM sqlite_schema WHERE type = 'table' ORDER BY name").fetchall())
