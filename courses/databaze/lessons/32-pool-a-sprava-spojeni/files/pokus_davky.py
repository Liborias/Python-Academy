"""Skutečný dvouřádkový pokus až s --pripojit; ponechá dva fiktivní řádky."""
import argparse
from contextlib import closing
import getpass
import uuid
from reseni import pridej_davku,prehled_z_poolu

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Dávka a skutečný rollback; vzniknou dva fiktivní řádky.')
    parser.add_argument('--pripojit',action='store_true')
    parser.add_argument('--heslo',action='store_true')
    args=parser.parse_args()
    if not args.pripojit:
        if args.heslo:parser.error('--heslo patří až k --pripojit.')
        from ukazka import ukaz_pool
        ukaz_pool(pridej_davku,prehled_z_poolu)
    else:
        heslo=getpass.getpass('Heslo PostgreSQL: ') if args.heslo else None
        try:
            from pg_podpora import priprav_pool
            with closing(priprav_pool(heslo)) as pool:
                from psycopg.errors import UniqueViolation
                prefix='Pokus-'+uuid.uuid4().hex[:12]
                a,b,c=[prefix+suffix for suffix in ('-A','-B','-C')]
                ids=pridej_davku(pool,[(a,2),(b,0)])
                print('Dva uložené fiktivní řádky, id:',ids)
                try:pridej_davku(pool,[(c,1),(a,9)])
                except UniqueViolation:print('Konflikt: druhá dávka se vrací jako celek.')
                else:raise RuntimeError('Dávka s duplicitou měla selhat.')
                radky=[r for r in prehled_z_poolu(pool) if r[1].startswith(prefix)]
                if {r[1] for r in radky}!={a,b}:raise RuntimeError('Po konfliktu zůstal neúplný zápis.')
                print('Ověřeno: C neexistuje, A/B zůstaly. Pool je po chybě použitelný.')
        except (ValueError,RuntimeError) as chyba:parser.exit(2,f'Chyba: {chyba}\n')
        except Exception:parser.exit(2,'Pokus selhal. Ověřte nastavení přístupu, init a vlastní řešení.\n')
