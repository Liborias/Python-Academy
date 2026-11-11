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
