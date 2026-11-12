# Base64 je přenosový zápis, zlib komprese; ani jedno není šifrování.
import base64
import binascii
import zlib
from format_dat import MAX_TEXT, MAX_BALICEK, PREFIX, text_utf8

def zabal_text(text):
    data = text_utf8(text)
    return PREFIX + base64.b64encode(zlib.compress(data)).decode('ascii')

def rozbal_text(balicek):
    if not isinstance(balicek,str) or not balicek.startswith(PREFIX) or len(balicek)>MAX_BALICEK:
        raise ValueError('Neplatný formát balíčku z1.')
    payload = balicek[len(PREFIX):]
    try:
        data = base64.b64decode(payload, validate=True)
        if base64.b64encode(data).decode('ascii') != payload:
            raise ValueError('Base64 musí mít kanonický zápis.')
        dekoder = zlib.decompressobj()
        text = dekoder.decompress(data, MAX_TEXT+1)
        if len(text)>MAX_TEXT or not dekoder.eof or dekoder.unused_data or dekoder.unconsumed_tail:
            raise ValueError('Neúplný nebo příliš velký komprimovaný text.')
        return text.decode('utf-8')
    except (ValueError, binascii.Error, zlib.error, UnicodeError) as chyba:
        raise ValueError('Balíček nelze rozbalit jako omezený UTF-8 text.') from chyba
# Přenášíme fiktivní poznámku; neukazujeme žádné heslo ani jeho otisk.
if __name__ == '__main__':
    text = 'Žofie; poznámka\ndalší řádek'
    balicek = zabal_text(text)
    print('Formát:', balicek[:3], 'znaků:', len(balicek))
    print('Shodný text:', rozbal_text(balicek)==text)
