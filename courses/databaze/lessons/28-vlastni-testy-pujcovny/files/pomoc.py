def cisty_nazev(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Zadejte neprázdný text.')
    return text.strip()

def nezaporny_pocet(pocet):
    if type(pocet) is not int or pocet < 0:
        raise ValueError('Počet je nezáporný int, nikoli bool.')

def zkontroluj_schema(con):
    pozadovane = {
        'kategorie': {'id', 'nazev'},
        'pomucky': {'id', 'nazev', 'kusy', 'kategorie_id'},
        'vypujcky': {'id', 'pomucka_id', 'clen', 'vraceno'},
    }
    for tabulka, sloupce in pozadovane.items():
        nalezene = {r[1] for r in con.execute('PRAGMA table_info(' + tabulka + ')')}
        if not sloupce <= nalezene:
            raise ValueError('Použijte novou databázi projektu; staré schéma se automaticky nepřevádí.')
