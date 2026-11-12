import json
import sqlite3
from pravidla import PARAMETRY

# Veřejný náhradní záznam: umožní stejný scrypt krok pro neznámé jméno.
# Není to účet a jeho otisk není odvozený od uživatelova hesla.
NAHRADNI = {**PARAMETRY, 'sul':'00'*16, 'otisk':'00'*32}

def jmeno_uctu(jmeno):
    if not isinstance(jmeno,str):
        raise ValueError('Jméno musí být text.')
    kanonicke = jmeno.strip().casefold()
    if not kanonicke or len(kanonicke) > 64:
        raise ValueError('Jméno musí mít 1 až 64 znaků po sjednocení.')
    return kanonicke

def nacti_overeni(text):
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        return None

def over_poznamky(texty):
    if not isinstance(texty,list):
        raise ValueError('Předávejte seznam textových poznámek.')
    for text in texty:
        if not isinstance(text,str) or not text.strip() or len(text)>2000:
            raise ValueError('Poznámka musí mít 1 až 2000 znaků a obsahovat text.')
        try:
            text.encode('utf-8')
        except UnicodeError:
            raise ValueError('Poznámka musí být platný text UTF-8.') from None
    return list(texty)

def otevri_ucty(cesta):
    con = sqlite3.connect(cesta, autocommit=True)
    try:
        con.execute('PRAGMA foreign_keys=ON')
        if con.execute('PRAGMA foreign_keys').fetchone() != (1,):
            raise RuntimeError('Nelze zapnout vazby.')
        con.autocommit = False
        with con:
            con.execute('CREATE TABLE IF NOT EXISTS uzivatele(id INTEGER PRIMARY KEY,jmeno TEXT NOT NULL UNIQUE,overeni TEXT NOT NULL)')
            con.execute('CREATE TABLE IF NOT EXISTS poznamky(id INTEGER PRIMARY KEY,uzivatel_id INTEGER NOT NULL REFERENCES uzivatele(id) ON DELETE CASCADE,text TEXT NOT NULL)')
            for tabulka, potrebne in [('uzivatele',{'id','jmeno','overeni'}),('poznamky',{'id','uzivatel_id','text'})]:
                sloupce = {r[1] for r in con.execute(f'PRAGMA table_info({tabulka})')}
                if not potrebne <= sloupce:
                    raise ValueError('Jiné schéma: použijte nový ucty.sqlite3.')
        return con
    except Exception:
        con.close()
        raise
