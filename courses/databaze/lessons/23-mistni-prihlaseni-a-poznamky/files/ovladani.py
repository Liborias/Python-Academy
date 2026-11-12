"""Místní CLI: heslo čteme getpass, nikdy argumentem příkazové řádky."""
import argparse
from contextlib import closing
import getpass
from pathlib import Path
import sqlite3

def konzole(Ucty, Sezeni, soubor, prenos=None):
    parser = argparse.ArgumentParser(description='Místní cvičné účty a poznámky')
    parser.add_argument('--db', default=str(Path(soubor).with_name('ucty.sqlite3')))
    prikazy = parser.add_subparsers(dest='prikaz', required=True)
    r = prikazy.add_parser('registrace');r.add_argument('jmeno')
    p = prikazy.add_parser('prihlaseni');p.add_argument('jmeno')
    if prenos:
        for jmeno in ('export','import'):
            p = prikazy.add_parser(jmeno);p.add_argument('jmeno');p.add_argument('cesta')
    args = parser.parse_args()
    try:
        with closing(Ucty(args.db)) as model:
            heslo = getpass.getpass('Cvičné heslo: ')
            if args.prikaz=='registrace':
                if heslo != getpass.getpass('Zopakujte heslo: '):
                    raise ValueError('Hesla se neshodují.')
                print('Účet ID:', model.registruj(args.jmeno, heslo))
                return
            sezeni = Sezeni(model)
            if not sezeni.prihlas(args.jmeno,heslo):
                raise ValueError('Přihlášení se nezdařilo.')
            try:
                if args.prikaz in ('export','import'):
                    print('Počet poznámek:', prenos(args.prikaz,sezeni,args.cesta))
                    return
                print('Přihlášen:', sezeni.uzivatel[1])
                while True:
                    volba = input('1 Výpis, 2 Přidat, 3 Odhlásit: ').strip()
                    if volba=='1':
                        for ident,text in sezeni.seznam():print(ident,text)
                    elif volba=='2':
                        sezeni.uloz(input('Poznámka: '));print('Poznámka uložena.')
                    elif volba=='3':
                        break
                    else:
                        print('Zvolte 1, 2 nebo 3.')
            finally:
                sezeni.odhlas()
    except (sqlite3.Error,OSError,ValueError,EOFError) as chyba:
        parser.exit(2, f'Chyba: {chyba}\n')
    except KeyboardInterrupt:
        parser.exit(130, 'Ukončeno.\n')
