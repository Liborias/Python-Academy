# Cesty počítáme bez zápisu, záloha používá SQLite API nad potvrzeným modelem.
from pathlib import Path
from contextlib import closing
import sqlite3
from tempfile import TemporaryDirectory
from model import Pujcovna
from soubory import bezpecny_cil

def cesty_projektu(soubor, db=None):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')

def zaloha_projektu(model, cesta):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')
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
