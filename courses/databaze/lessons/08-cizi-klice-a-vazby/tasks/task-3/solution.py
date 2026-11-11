# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from podklady import priprav_texty, priprav_souhrny, priprav_vazby
from relacni_schema import spojeni_s_vazbami

def zapis_pomucku(con, nazev, kusy, kategorie_id=None):
    return con.execute('INSERT INTO pomucky (nazev, kusy, kategorie_id) VALUES (?, ?, ?)',
                       (nazev, kusy, kategorie_id)).lastrowid

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(spojeni_s_vazbami(':memory:')) as con:
        with con:
            priprav_vazby(con)
            print('Nové ID:', zapis_pomucku(con, 'Míč', 2, 7))
