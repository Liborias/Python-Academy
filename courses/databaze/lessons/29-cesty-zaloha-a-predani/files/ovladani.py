import argparse
from contextlib import closing
import sqlite3

def konzole(Model,soubor,cesty,zaloha,qr=None,final=False):
    p = argparse.ArgumentParser(description='Moje místní půjčovna')
    p.add_argument('--db')
    prikazy = p.add_subparsers(dest='prikaz')
    prikazy.add_parser('prehled')
    pridej = prikazy.add_parser('pridat');pridej.add_argument('nazev');pridej.add_argument('kusy',type=int)
    pujc = prikazy.add_parser('pujcit');pujc.add_argument('kod');pujc.add_argument('clen')
    vrat = prikazy.add_parser('vratit');vrat.add_argument('id',type=int)
    prikazy.add_parser('vypujcky')
    backup = prikazy.add_parser('zaloha');backup.add_argument('cesta')
    if final:
        export = prikazy.add_parser('export');export.add_argument('cesta')
    if qr:
        stitek = prikazy.add_parser('qr');stitek.add_argument('id',type=int);stitek.add_argument('cesta')
    args = p.parse_args()
    try:
        db = cesty(soubor,args.db)['db']
        with closing(Model(db)) as model:
            if args.prikaz=='pridat':
                ident = model.pridej_pomucku(args.nazev,args.kusy)
                print('Pomůcka ID:',ident,'kód:',model.kod(ident))
            elif args.prikaz=='pujcit':print('Výpůjčka ID:',model.pujc_kod(args.kod,args.clen))
            elif args.prikaz=='vratit':print('Vráceno:',model.vrat(args.id))
            elif args.prikaz=='vypujcky':
                for radek in model.aktivni_vypujcky():print(radek)
            elif args.prikaz=='zaloha':print('Záloha:',zaloha(model,args.cesta))
            elif args.prikaz=='export':print('Exportováno:',model.stitky_csv(args.cesta))
            elif args.prikaz=='qr':
                payload = 'PY-AKADEMIE:PUJ:'+model.kod(args.id)
                cil = qr(payload,args.cesta,zdroj=model.cesta)
                if cil is None:raise ValueError('QR je volitelný: doinstalujte qrcode[pil]>=8.2,<9.')
                print('QR:',cil)
            else:
                for radek in (model.karty() if final else model.prehled()):print(radek)
    except (ValueError,sqlite3.Error,OSError) as chyba:
        p.exit(2,f'Chyba: {chyba}\n')
