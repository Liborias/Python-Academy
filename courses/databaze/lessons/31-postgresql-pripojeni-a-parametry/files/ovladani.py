"""Bez --pripojit se provede jen simulace; --help nic nepřipojuje."""
import argparse
from contextlib import closing
import getpass
import sys

def spust(pridej,prehled,*,pool=False):
    p=argparse.ArgumentParser(description='Volitelný PostgreSQL inventář')
    p.add_argument('--pripojit',action='store_true',help='výslovně použít vlastní PostgreSQL podle PG*')
    p.add_argument('--heslo',action='store_true',help='zeptat se přes getpass bez echa; heslo se nepíše za přepínač')
    sub=p.add_subparsers(dest='prikaz')
    sub.add_parser('init',help='vytvořit cvičnou tabulku, existující data ponechat')
    a=sub.add_parser('pridat');a.add_argument('nazev');a.add_argument('kusy',type=int)
    a=sub.add_parser('prehled');a.add_argument('--minimum',type=int,default=0)
    args=p.parse_args()
    if not args.pripojit:
        if args.heslo or args.prikaz:p.error('Pro skutečný příkaz přidejte --pripojit. Bez něj běží pouze simulace.')
        from ukazka import ukaz_pg,ukaz_pool
        return (ukaz_pool if pool else ukaz_pg)(pridej,prehled)
    if not args.prikaz:p.error('Vyberte init, pridat nebo prehled.')
    heslo=getpass.getpass('Heslo PostgreSQL: ') if args.heslo else None
    try:
        from pg_podpora import pripoj,priprav_pool,vytvor_tabulku
        if pool:
            with closing(priprav_pool(heslo)) as zasobnik:
                if args.prikaz=='init':
                    with zasobnik.connection(timeout=3) as con:vytvor_tabulku(con)
                elif args.prikaz=='pridat':print('ID dávky:',pridej(zasobnik,[(args.nazev,args.kusy)]))
                else:
                    for radek in prehled(zasobnik,args.minimum):print(radek)
        else:
            with pripoj(heslo) as con:
                if args.prikaz=='init':vytvor_tabulku(con)
                elif args.prikaz=='pridat':print('Pomůcka ID:',pridej(con,args.nazev,args.kusy))
                else:
                    for radek in prehled(con,args.minimum):print(radek)
        print('Hotovo; vlastní spojení/pool je uzavřený.')
    except (ValueError,RuntimeError) as chyba:p.exit(2,f'Chyba: {chyba}\n')
    except Exception:
        p.exit(2,'Databázová operace selhala. Ověřte server, přístup, SQL a jedinečný název; podrobnosti přístupu se nevypisují.\n')
