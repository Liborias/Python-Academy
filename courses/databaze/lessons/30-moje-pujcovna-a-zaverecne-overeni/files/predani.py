# Cesty počítáme bez zápisu, záloha používá SQLite API nad potvrzeným modelem.
from pathlib import Path
from contextlib import closing
import sqlite3
from tempfile import TemporaryDirectory
from model import Pujcovna
from soubory import bezpecny_cil

def cesty_projektu(soubor, db=None):
    koren = Path(soubor).resolve().parent
    databaze = koren/'pujcovna.sqlite3' if db is None else Path(db).expanduser().resolve()
    return {'koren':koren,'db':databaze}

def zaloha_projektu(model, cesta):
    with bezpecny_cil(cesta,model.cesta) as (docasny,cil):
        with closing(sqlite3.connect(docasny,autocommit=True)) as target:
            model.con.backup(target)
    return cil
