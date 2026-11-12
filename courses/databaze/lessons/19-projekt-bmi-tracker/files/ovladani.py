"""CLI bez grafických importů; Tk potřebujeme teprve pro větev s oknem."""
import argparse
from contextlib import closing
from pathlib import Path
import sqlite3

def konzole(Tracker, soubor, Aplikace=None, soubory=True):
    parser = argparse.ArgumentParser(description='Místní BMI tracker')
    parser.add_argument('--db', default=str(Path(soubor).with_name('bmi.sqlite3')))
    prikazy = parser.add_subparsers(dest='prikaz')
    prikazy.add_parser('gui')
    if soubory:
        export = prikazy.add_parser('export')
        export.add_argument('cesta')
        export.add_argument('--od')
        export.add_argument('--do')
        zaloha = prikazy.add_parser('zaloha')
        zaloha.add_argument('cesta')
    args = parser.parse_args()
    try:
        if args.prikaz in ('export','zaloha'):
            with closing(Tracker(args.db)) as model:
                if args.prikaz == 'export':
                    print('Exportováno řádků:', model.export_csv(args.cesta, args.od, args.do))
                else:
                    print('Záloha:', model.zaloha(args.cesta))
        else:
            try:
                from spousteni import spust
                if Aplikace is None:
                    from aplikace import Aplikace
            except ImportError:
                raise ValueError('Pro okno vyberte Python s Tkinterem.') from None
            spust(Aplikace, Tracker, args.db)
    except (sqlite3.Error, OSError, ValueError) as chyba:
        parser.exit(2, f'Chyba: {chyba}\n')
