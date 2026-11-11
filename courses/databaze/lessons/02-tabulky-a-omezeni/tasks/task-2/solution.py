# SQLite je součást standardní knihovny; spojení nepotřebuje síťový server.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

def vytvor_kategorie(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS kategorie (
            id INTEGER PRIMARY KEY,
            nazev TEXT NOT NULL UNIQUE
        )
    ''')

# Při importu nic neotevíráme; ukázka pracuje jen s cvičnými daty.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        vytvor_kategorie(con)
        con.execute('INSERT INTO kategorie (nazev) VALUES (?)', ('Sport',))
        print(con.execute('SELECT id, nazev FROM kategorie').fetchall())
