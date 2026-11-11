# Používáme skutečné SQLite ze standardní knihovny, bez síťového serveru.
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from podklady import priprav_texty, priprav_souhrny, priprav_vazby

def zkus_typy(hodnoty):
    # Doplňte podle zadání, SQL hodnoty patří do parametrů.
    raise NotImplementedError

# Ukázka se provede jen při spuštění souboru, nikoli při importu.
if __name__ == '__main__':
    print(zkus_typy(['003', 2.0, 'ahoj', None]))
