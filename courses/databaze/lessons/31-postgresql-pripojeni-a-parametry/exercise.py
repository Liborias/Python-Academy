# Doplňte vlastní řešení podle výkladu.
from validace import nazev_pomucky, pocet_kusu

def pridej_pg(con, nazev, kusy):
    raise NotImplementedError('Doplňte podle zadání.')

def prehled_pg(con, minimum=0):
    raise NotImplementedError('Doplňte podle zadání.')
if __name__ == '__main__':
    from ukazka import ukaz_pg
    ukaz_pg(pridej_pg, prehled_pg)
