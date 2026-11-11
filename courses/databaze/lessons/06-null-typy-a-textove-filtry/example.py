# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from podklady import priprav_texty, priprav_souhrny, priprav_vazby

def bez_poznamky(con):
    return con.execute('SELECT id, popis FROM udalosti WHERE poznamka IS NULL ORDER BY id').fetchall()

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        priprav_texty(con)
        print(bez_poznamky(con))
