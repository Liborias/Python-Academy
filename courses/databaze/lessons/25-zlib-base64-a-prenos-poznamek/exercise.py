# Base64 je přenosový zápis, zlib komprese; ani jedno není šifrování.
import base64
import binascii
import zlib
from format_dat import MAX_TEXT, MAX_BALICEK, PREFIX, text_utf8

def zabal_text(text):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')

def rozbal_text(balicek):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')
# Přenášíme fiktivní poznámku; neukazujeme žádné heslo ani jeho otisk.
if __name__ == '__main__':
    text = 'Žofie; poznámka\ndalší řádek'
    balicek = zabal_text(text)
    print('Formát:', balicek[:3], 'znaků:', len(balicek))
    print('Shodný text:', rozbal_text(balicek)==text)
