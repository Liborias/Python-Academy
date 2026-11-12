# Ukládáme sůl a nákladně odvozený otisk, nikoli původní heslo.
import hashlib
import hmac
import secrets
from pravidla import PARAMETRY, MAXMEM, over_heslo_text, over_zaznam

def vytvor_zaznam(heslo):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')

def over_heslo(heslo, zaznam):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')
# Pouze fiktivní fráze; výpis neobsahuje heslo ani samotný otisk.
if __name__ == '__main__':
    zaznam = vytvor_zaznam('Cvičná fráze pro lekci!')
    print('Algoritmus:', zaznam['algoritmus'], 'N:', zaznam['n'])
    print('Sůl bajtů:', len(bytes.fromhex(zaznam['sul'])))
    print('Správné:', over_heslo('Cvičná fráze pro lekci!', zaznam))
    print('Nesprávné:', over_heslo('Jiná cvičná fráze!', zaznam))
