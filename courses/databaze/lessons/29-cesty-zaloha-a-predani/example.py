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
# Vlastní soubory neměníme: nová složka se po ukázce uklidí.
if __name__ == '__main__':
    print('Výchozí jméno DB:', cesty_projektu(__file__)['db'].name)
    with TemporaryDirectory() as temp:
        cil = Path(temp)/'kopie.sqlite3'
        with closing(Pujcovna(':memory:')) as model:
            model.pridej_pomucku('Míč',2)
            zaloha_projektu(model,cil)
        with closing(Pujcovna(cil)) as kopie:
            print('Znovu otevřená záloha:', kopie.prehled())
