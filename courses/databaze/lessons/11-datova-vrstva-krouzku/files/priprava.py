import sqlite3

def cisty_nazev(hodnota):
    if not isinstance(hodnota, str) or not hodnota.strip():
        raise ValueError('Napište neprázdný název nebo jméno.')
    return hodnota.strip()

def kladna_kapacita(hodnota):
    if type(hodnota) is not int or hodnota <= 0:
        raise ValueError('Kapacita musí být kladné celé číslo.')
    return hodnota

def cti_kapacitu(text):
    try:
        hodnota = int(text)
    except ValueError:
        raise ValueError('Kapacita musí být kladné celé číslo.') from None
    return kladna_kapacita(hodnota)

def otevri_krouzky(cesta):
    con = sqlite3.connect(cesta, autocommit=True)
    try:
        con.execute('PRAGMA foreign_keys = ON')
        if con.execute('PRAGMA foreign_keys').fetchone() != (1,):
            raise RuntimeError('Nepodařilo se zapnout vazby.')
        con.autocommit = False
        with con:
            con.execute('''CREATE TABLE IF NOT EXISTS krouzky (
                id INTEGER PRIMARY KEY, nazev TEXT NOT NULL UNIQUE,
                kapacita INTEGER NOT NULL CHECK(typeof(kapacita)='integer' AND kapacita>0))''')
            con.execute('''CREATE TABLE IF NOT EXISTS prihlasky (
                id INTEGER PRIMARY KEY,
                krouzek_id INTEGER NOT NULL REFERENCES krouzky(id) ON DELETE RESTRICT,
                clen TEXT NOT NULL, UNIQUE(krouzek_id, clen))''')
            for tabulka, potrebne in [('krouzky', {'id','nazev','kapacita'}),
                                      ('prihlasky', {'id','krouzek_id','clen'})]:
                # Jméno tabulky je z tohoto pevného seznamu, nikoli od uživatele.
                sloupce = {r[1] for r in con.execute(f'PRAGMA table_info({tabulka})')}
                if not potrebne <= sloupce:
                    raise ValueError('Soubor má jiné schéma. Zvolte nový krouzky.sqlite3.')
        return con
    except Exception:
        con.close()
        raise
