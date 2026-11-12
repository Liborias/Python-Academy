from pathlib import Path

def over_qr_text(text):
    if not isinstance(text,str) or not text.strip():
        raise ValueError('QR potřebuje neprázdný text.')
    try:
        data = text.encode('utf-8')
    except UnicodeError:
        raise ValueError('QR potřebuje platné UTF-8.') from None
    if len(data)>512:
        raise ValueError('QR text smí mít nejvýše 512 bajtů UTF-8.')
    return data

def cil_png(cesta):
    cil = Path(cesta).resolve()
    if cil.suffix.lower() != '.png':
        raise ValueError('Pro QR zvolte soubor .png.')
    return cil

def ziskej_qrcode():
    try:
        import qrcode
        import PIL.Image
    except ModuleNotFoundError as chyba:
        if chyba.name == 'qrcode' or chyba.name == 'PIL' or chyba.name.startswith('PIL.'):
            return None
        raise
    return qrcode
