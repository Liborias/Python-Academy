"""Skutečné připojení je jen na výslovný požadavek uloženého spouštěče."""
import os

def pristup():
    chybi=[k for k in ['PGHOST','PGPORT','PGDATABASE','PGUSER'] if not os.environ.get(k)]
    if chybi:raise ValueError('Nastavte PGHOST, PGPORT, PGDATABASE a PGUSER podle NAVOD.md.')
    return {'autocommit':True,'connect_timeout':5,'application_name':'python-akademie'}

def pripoj(heslo=None):
    nastaveni=pristup()
    try:import psycopg
    except ModuleNotFoundError:
        raise RuntimeError('Doinstalujte psycopg[binary,pool]>=3.2,<4 do stejné .venv.') from None
    if heslo is not None:nastaveni['password']=heslo
    return psycopg.connect('',**nastaveni)

def vytvor_tabulku(con):
    with con.transaction():
        con.execute("""CREATE TABLE IF NOT EXISTS akademie_pomucky(
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nazev TEXT NOT NULL UNIQUE,
            kusy INTEGER NOT NULL CHECK(kusy>=0))""")

def priprav_pool(heslo=None):
    nastaveni=pristup()
    try:from psycopg_pool import ConnectionPool
    except (ModuleNotFoundError,ImportError):
        raise RuntimeError('Doinstalujte psycopg[binary,pool]>=3.2,<4 do stejné .venv.') from None
    if heslo is not None:nastaveni['password']=heslo
    pool=ConnectionPool('',min_size=1,max_size=3,timeout=3,kwargs=nastaveni,open=False)
    try:pool.open(wait=True,timeout=8)
    except BaseException:pool.close();raise
    return pool
