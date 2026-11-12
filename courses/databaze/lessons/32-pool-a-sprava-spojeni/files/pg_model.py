from validace import nazev_pomucky, pocet_kusu

def pridej_pg(con, nazev, kusy):
    nazev = nazev_pomucky(nazev)
    kusy = pocet_kusu(kusy)
    with con.transaction():
        with con.cursor() as cur:
            cur.execute('INSERT INTO akademie_pomucky(nazev,kusy) VALUES(%s,%s) RETURNING id', (nazev, kusy))
            return cur.fetchone()[0]

def prehled_pg(con, minimum=0):
    minimum = pocet_kusu(minimum)
    with con.transaction():
        with con.cursor() as cur:
            cur.execute('SELECT id,nazev,kusy FROM akademie_pomucky WHERE kusy >= %s ORDER BY id', (minimum,))
            return cur.fetchall()
