# Pool vlastní spojení, funkce si je pouze na chvíli půjčí.
from validace import pocet_kusu, priprav_davku
from pg_model import pridej_pg, prehled_pg

def prehled_z_poolu(pool, minimum=0):
    minimum = pocet_kusu(minimum)
    with pool.connection(timeout=3) as con:
        return prehled_pg(con,minimum)

def pridej_davku(pool, pomucky):
    pomucky = priprav_davku(pomucky)
    if not pomucky:
        return []
    with pool.connection(timeout=3) as con:
        with con.transaction():
            return [pridej_pg(con,nazev,kusy) for nazev,kusy in pomucky]

# Výukový pool je označená simulace, skutečný server má samostatný spouštěč.
if __name__ == '__main__':
    from ukazka import ukaz_pool
    ukaz_pool(pridej_davku,prehled_z_poolu)
