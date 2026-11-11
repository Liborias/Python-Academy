# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from podklady import priprav_texty, priprav_souhrny, priprav_vazby
from relacni_schema import spojeni_s_vazbami
from relacni_schema import vytvor_relacni_schema

def prehled_kategorii(con):
    return con.execute('''
        SELECT k.id, k.nazev, COUNT(p.id), COALESCE(SUM(p.kusy), 0)
        FROM kategorie AS k LEFT JOIN pomucky AS p ON p.kategorie_id = k.id
        GROUP BY k.id, k.nazev ORDER BY k.id
    ''').fetchall()

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    with closing(spojeni_s_vazbami(':memory:')) as con:
        with con:
            priprav_vazby(con)
            print(prehled_kategorii(con))
