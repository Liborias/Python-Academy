"""Krátké běhy vždy zůstávají offline, bez ohledu na proměnné PG*."""
from demonstrace import DemoSpojeni,DemoPool,DemoIntegrita

def ukaz_pg(pridej,prehled):
    print('VÝUKOVÁ SIMULACE: PostgreSQL server se nepřipojuje.')
    con=DemoSpojeni()
    try:
        print('ID:',pridej(con,"Karty O'Neil",2))
        print('ID:',pridej(con,'Krabice',0))
        print('Vše:',prehled(con))
        print('Alespoň 1 kus:',prehled(con,1))
        print('Parametry jsou oddělené od SQL, spojení stále používá volající.')
    finally:con.close()

def ukaz_pool(pridej,prehled):
    print('VÝUKOVÁ SIMULACE: pool zde nepřipojuje skutečný server.')
    pool=DemoPool()
    try:
        print('ID dávky:',pridej(pool,[("Karty O'Neil",2),('Krabice',0)]))
        try:pridej(pool,[('Míč',3),('Krabice',1)])
        except DemoIntegrita:print('Duplicitní název: celá druhá dávka vrácena.')
        print('Přehled:',prehled(pool))
        print('Převzetí/vrácení:',pool.prevzeti,pool.vraceni,'právě půjčeno:',pool.vypujceno)
        print('Pool vlastní a zavře až volající.')
    finally:pool.close()
