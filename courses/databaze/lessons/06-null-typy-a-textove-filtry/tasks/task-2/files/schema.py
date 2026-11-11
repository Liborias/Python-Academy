def vytvor_pomucky(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS pomucky (
            id INTEGER PRIMARY KEY,
            nazev TEXT NOT NULL UNIQUE,
            kusy INTEGER NOT NULL DEFAULT 0 CHECK (kusy >= 0)
        )
    ''')
def vytvor_kategorie(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS kategorie (
            id INTEGER PRIMARY KEY,
            nazev TEXT NOT NULL UNIQUE
        )
    ''')
def vytvor_vypujcky(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS vypujcky (
            id INTEGER PRIMARY KEY,
            pomucka TEXT NOT NULL,
            clen TEXT NOT NULL,
            vraceno INTEGER NOT NULL DEFAULT 0 CHECK (vraceno IN (0, 1))
        )
    ''')
def vytvor_udalosti(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS udalosti (
            id INTEGER PRIMARY KEY,
            popis TEXT NOT NULL,
            poznamka TEXT
        )
    ''')
