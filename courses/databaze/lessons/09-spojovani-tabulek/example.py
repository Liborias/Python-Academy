# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from podklady import priprav_texty, priprav_souhrny, priprav_vazby
from relacni_schema import spojeni_s_vazbami
from relacni_schema import vytvor_relacni_schema

def pomucky_s_kategorii(con):
    return con.execute('''
        SELECT p.id, p.nazev, p.kusy, k.nazev
        FROM pomucky AS p JOIN kategorie AS k ON p.kategorie_id = k.id
        ORDER BY p.id
    ''').fetchall()

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(spojeni_s_vazbami(':memory:')) as con:
        with con:
            priprav_vazby(con)
            print(pomucky_s_kategorii(con))
