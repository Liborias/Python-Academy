# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

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
