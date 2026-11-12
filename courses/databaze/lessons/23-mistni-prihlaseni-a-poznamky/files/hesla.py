# Ukládáme sůl a nákladně odvozený otisk, nikoli původní heslo.
import hashlib
import hmac
import secrets
from pravidla import PARAMETRY, MAXMEM, over_heslo_text, over_zaznam

def vytvor_zaznam(heslo):
    data = over_heslo_text(heslo)
    sul = secrets.token_bytes(16)
    otisk = hashlib.scrypt(data, salt=sul, n=PARAMETRY['n'], r=8, p=1,
                          dklen=32, maxmem=MAXMEM)
    return {**PARAMETRY, 'sul':sul.hex(), 'otisk':otisk.hex()}

def over_heslo(heslo, zaznam):
    try:
        data = over_heslo_text(heslo)
    except ValueError:
        return False
    if not over_zaznam(zaznam):
        return False
    sul = bytes.fromhex(zaznam['sul'])
    ocekavany = bytes.fromhex(zaznam['otisk'])
    skutecny = hashlib.scrypt(data, salt=sul, n=PARAMETRY['n'], r=8, p=1,
                              dklen=32, maxmem=MAXMEM)
    return hmac.compare_digest(skutecny, ocekavany)
