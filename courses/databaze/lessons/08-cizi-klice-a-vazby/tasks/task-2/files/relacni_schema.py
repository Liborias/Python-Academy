# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

def spojeni_s_vazbami(cesta):
    con = sqlite3.connect(cesta, autocommit=True)
    try:
        con.execute('PRAGMA foreign_keys = ON')
        if con.execute('PRAGMA foreign_keys').fetchone()[0] != 1:
            raise RuntimeError('Cizí klíče se nepodařilo zapnout.')
        con.autocommit = False
        return con
    except Exception:
        con.close()
        raise
