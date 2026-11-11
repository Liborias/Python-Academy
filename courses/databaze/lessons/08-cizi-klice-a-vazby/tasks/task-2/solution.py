# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from relacni_schema import spojeni_s_vazbami

def vytvor_relacni_schema(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS kategorie (
            id INTEGER PRIMARY KEY,
            nazev TEXT NOT NULL UNIQUE
        )
    ''')
    con.execute('''
        CREATE TABLE IF NOT EXISTS pomucky (
            id INTEGER PRIMARY KEY,
            nazev TEXT NOT NULL UNIQUE,
            kusy INTEGER NOT NULL CHECK (typeof(kusy) = 'integer' AND kusy >= 0),
            kategorie_id INTEGER REFERENCES kategorie(id) ON DELETE SET NULL
        )
    ''')
    con.execute('''
        CREATE TABLE IF NOT EXISTS vypujcky (
            id INTEGER PRIMARY KEY,
            pomucka_id INTEGER NOT NULL REFERENCES pomucky(id) ON DELETE RESTRICT,
            clen TEXT NOT NULL,
            vraceno INTEGER NOT NULL DEFAULT 0 CHECK (vraceno IN (0, 1))
        )
    ''')

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(spojeni_s_vazbami(':memory:')) as con:
        with con:
            vytvor_relacni_schema(con)
            print(con.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall())
