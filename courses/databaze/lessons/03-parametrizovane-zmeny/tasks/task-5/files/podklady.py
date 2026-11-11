from schema import vytvor_pomucky, vytvor_udalosti

def priprav_sklad(con):
    # Volejte nad novou cvičnou databází, existující řádky se nemažou.
    vytvor_pomucky(con)
    vytvor_udalosti(con)
    con.executemany('INSERT INTO pomucky (id, nazev, kusy) VALUES (?, ?, ?)',
                   [(10, 'Šachy', 2), (3, 'Míče', 0), (21, 'Lana', 5)])

def vyzaduj_transakce(con):
    if con.autocommit is not False:
        raise ValueError('Použijte spojení s autocommit=False.')

def kladny_pocet(kolik):
    if type(kolik) is not int or kolik <= 0:
        raise ValueError('Počet musí být kladné celé číslo.')
