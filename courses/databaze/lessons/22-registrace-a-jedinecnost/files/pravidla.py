"""Pevná verze odvozování: parametry ze záznamu nemohou zvýšit nároky výpočtu."""
import re

PARAMETRY = {'verze':1, 'algoritmus':'scrypt', 'n':2**17, 'r':8, 'p':1, 'dklen':32}
MAXMEM = 256 * 1024 * 1024

def over_heslo_text(heslo):
    if not isinstance(heslo, str) or not 12 <= len(heslo) <= 256:
        raise ValueError('Cvičné heslo musí mít 12 až 256 znaků.')
    try:
        data = heslo.encode('utf-8')
    except UnicodeError:
        raise ValueError('Heslo musí být platný text UTF-8.') from None
    if len(data) > 1024:
        raise ValueError('Heslo je v UTF-8 příliš dlouhé.')
    return data  # Heslo neořezáváme, nenormalizujeme ani nelogujeme.

def over_zaznam(zaznam):
    if not isinstance(zaznam, dict) or set(zaznam) != set(PARAMETRY) | {'sul','otisk'}:
        return False
    for klic, hodnota in PARAMETRY.items():
        if type(zaznam[klic]) is not type(hodnota) or zaznam[klic] != hodnota:
            return False
    return (isinstance(zaznam['sul'], str) and re.fullmatch('[0-9a-f]{32}', zaznam['sul']) is not None
            and isinstance(zaznam['otisk'], str) and re.fullmatch('[0-9a-f]{64}', zaznam['otisk']) is not None)
