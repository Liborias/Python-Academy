from datetime import date
import sqlite3
from vypocet import bmi
from validace import kladne_cislo

def over_datum(den):
    if not isinstance(den, str):
        raise ValueError('Datum napište jako RRRR-MM-DD.')
    try:
        platny = date.fromisoformat(den)
    except ValueError:
        raise ValueError('Datum musí existovat a mít tvar RRRR-MM-DD.') from None
    if platny.isoformat() != den:
        raise ValueError('Datum napište přesně jako RRRR-MM-DD.')
    return den

def over_mereni(den, hmotnost, vyska_cm, poznamka):
    den = over_datum(den)
    hmotnost = kladne_cislo(hmotnost)
    vyska_cm = kladne_cislo(vyska_cm)
    bmi(hmotnost, vyska_cm)
    if not isinstance(poznamka, str):
        raise ValueError('Poznámka musí být text.')
    return den, hmotnost, vyska_cm, poznamka

def otevri_tracker(cesta):
    con = sqlite3.connect(cesta, autocommit=False)
    try:
        with con:
            con.execute('''CREATE TABLE IF NOT EXISTS mereni (
                id INTEGER PRIMARY KEY, den TEXT NOT NULL,
                hmotnost REAL NOT NULL CHECK(hmotnost>0),
                vyska_cm REAL NOT NULL CHECK(vyska_cm>0),
                poznamka TEXT NOT NULL DEFAULT '')''')
            sloupce = {r[1] for r in con.execute('PRAGMA table_info(mereni)')}
            if not {'id','den','hmotnost','vyska_cm','poznamka'} <= sloupce:
                raise ValueError('Soubor má jiné schéma. Zvolte nový bmi.sqlite3.')
        return con
    except Exception:
        con.close()
        raise
