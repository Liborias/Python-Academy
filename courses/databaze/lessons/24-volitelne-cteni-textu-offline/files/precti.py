import argparse
from reseni import precti

p=argparse.ArgumentParser(description='Volitelná offline řeč')
p.add_argument('text',nargs='?',default='Ukázková poznámka.')
p.add_argument('--mluv',action='store_true')
if __name__ == '__main__':
    a=p.parse_args()
    try:
        stav=precti(a.text,mluv=a.mluv)
    except ValueError as chyba:
        p.exit(2,f'Chyba: {chyba}\n')
    print('Režim:',stav)
    raise SystemExit(2 if stav=='nedostupne' else 0)
