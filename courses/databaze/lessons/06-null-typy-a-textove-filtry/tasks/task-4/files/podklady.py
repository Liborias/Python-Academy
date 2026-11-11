from schema import vytvor_pomucky, vytvor_udalosti

def priprav_texty(con):
    vytvor_pomucky(con)
    vytvor_udalosti(con)
    con.executemany('INSERT INTO pomucky (id,nazev,kusy) VALUES (?,?,?)',
        [(3,'Šachy',2),(8,'Karty 100%',0),(11,'Míč_A',5),(20,'Karty O\'Neil',1)])
    con.executemany('INSERT INTO udalosti (id,popis,poznamka) VALUES (?,?,?)',
        [(1,'Otevřeno',None),(4,'Kontrola',''),(7,'Dar','Žofie'),(9,'Další dar','Žofie')])

def priprav_souhrny(con):
    con.execute('CREATE TABLE pomucky (id INTEGER PRIMARY KEY,nazev TEXT NOT NULL,kusy INTEGER NOT NULL,kategorie TEXT)')
    vytvor_udalosti(con)
    con.executemany('INSERT INTO pomucky VALUES (?,?,?,?)',
        [(3,'Šachy',2,'Hry'),(8,'Karty',0,'Hry'),(11,'Lana',5,'Sport'),(20,'Míče',1,'Sport'),(30,'Krabice',3,None)])
    con.executemany('INSERT INTO udalosti (popis,poznamka) VALUES (?,?)',
        [('Bez poznámky',None),('Prázdná',''),('Dar','Žofie'),('Další dar','Žofie')])

def priprav_vazby(con):
    from relacni_schema import vytvor_relacni_schema
    vytvor_relacni_schema(con)
    con.executemany('INSERT INTO kategorie(id,nazev) VALUES (?,?)',[(2,'Hry'),(7,'Sport'),(15,'Prázdná')])
    con.executemany('INSERT INTO pomucky(id,nazev,kusy,kategorie_id) VALUES (?,?,?,?)',
        [(3,'Šachy',2,2),(8,'Karty',0,2),(11,'Lana',5,7),(20,'Krabice',1,None)])
    con.executemany('INSERT INTO vypujcky(id,pomucka_id,clen,vraceno) VALUES (?,?,?,?)',
        [(1,3,'Žofie',0),(4,3,'Ada',1),(7,11,'Žofie',1),(9,8,'Ada',0)])
