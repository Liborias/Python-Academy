import argparse
from contextlib import closing
from pathlib import Path
import sqlite3

def main(Evidence):
    parser = argparse.ArgumentParser(description='Klubovní evidence pomůcek a výpůjček')
    parser.add_argument('--db', default=str(Path(__file__).with_name('klub.sqlite3')))
    prikazy = parser.add_subparsers(dest='prikaz')
    prikazy.add_parser('prehled')
    k = prikazy.add_parser('kategorie')
    k.add_argument('nazev')
    p = prikazy.add_parser('pomucka')
    p.add_argument('nazev')
    p.add_argument('kusy', type=int)
    p.add_argument('--kategorie', type=int)
    v = prikazy.add_parser('pujcit')
    v.add_argument('id', type=int)
    v.add_argument('clen')
    r = prikazy.add_parser('vratit')
    r.add_argument('id', type=int)
    prikazy.add_parser('vypujcky')
    args = parser.parse_args()
    try:
        with closing(Evidence(args.db)) as klub:
            if args.prikaz == 'kategorie':
                print('Kategorie ID:', klub.pridej_kategorii(args.nazev))
            elif args.prikaz == 'pomucka':
                print('Pomůcka ID:', klub.pridej_pomucku(args.nazev, args.kusy, args.kategorie))
            elif args.prikaz == 'pujcit':
                print('Výpůjčka ID:', klub.pujc(args.id, args.clen))
            elif args.prikaz == 'vratit':
                print('Vráceno:', klub.vrat(args.id))
            elif args.prikaz == 'vypujcky':
                for radek in klub.aktivni_vypujcky():print(radek)
            else:
                for radek in klub.prehled():print(radek)
        return 0
    except (ValueError, sqlite3.Error, OSError) as error:
        print('Chyba:', error)
        return 2
