# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

def vytvor_pomucky(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS pomucky (
            id INTEGER PRIMARY KEY,
            nazev TEXT NOT NULL UNIQUE,
            kusy INTEGER NOT NULL DEFAULT 0 CHECK (kusy >= 0)
        )
    ''')

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        vytvor_pomucky(con)
        print(con.execute('PRAGMA table_info(pomucky)').fetchall())
