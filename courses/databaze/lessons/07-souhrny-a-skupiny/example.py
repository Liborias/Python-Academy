# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from podklady import priprav_texty, priprav_souhrny, priprav_vazby

def celkovy_souhrn(con):
    return con.execute('SELECT COUNT(*), COALESCE(SUM(kusy), 0), MIN(kusy), MAX(kusy) FROM pomucky').fetchone()

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
        priprav_souhrny(con)
        print(celkovy_souhrn(con))
