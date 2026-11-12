# Doplňte vlastní řešení podle výkladu.
from validace import pocet_kusu, priprav_davku
from pg_model import pridej_pg, prehled_pg

def prehled_z_poolu(pool, minimum=0):
    raise NotImplementedError('Doplňte podle zadání.')

def pridej_davku(pool, pomucky):
    raise NotImplementedError('Doplňte podle zadání.')
if __name__ == '__main__':
    from ukazka import ukaz_pool
    ukaz_pool(pridej_davku, prehled_z_poolu)
