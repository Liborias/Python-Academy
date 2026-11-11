# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from relacni_schema import spojeni_s_vazbami

def vytvor_relacni_schema(con):
    # Doplňte podle zadání, SQL hodnoty patří do parametrů.
    raise NotImplementedError

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(spojeni_s_vazbami(':memory:')) as con:
        with con:
            vytvor_relacni_schema(con)
            print(con.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall())
