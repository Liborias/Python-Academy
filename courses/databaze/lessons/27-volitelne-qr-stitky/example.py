# Obsah QR zůstává lokální; nic neotevíráme a nikam jej neposíláme.
from qr_podpora import over_qr_text, cil_png, ziskej_qrcode
from soubory import bezpecny_cil

def qr_png(text, cesta, *, zdroj=None):
    data = over_qr_text(text)
    cil = cil_png(cesta)
    knihovna = ziskej_qrcode()
    if knihovna is None:
        return None
    with bezpecny_cil(cil, zdroj) as (docasny, cil):
        qr = knihovna.QRCode(error_correction=knihovna.constants.ERROR_CORRECT_M,
                            box_size=6, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        obrazek = qr.make_image(fill_color='black', back_color='white')
        obrazek.save(docasny, format='PNG')
    return cil
# V Akademii vznikne PNG v dočasném běhu; pro vlastní soubor uložte pracovní složku.
if __name__ == '__main__':
    cil = qr_png('PY-AKADEMIE:PUJ:18', 'stitek.png')
    if cil is None:
        print('QR je volitelný. Doinstalujte qrcode[pil]>=8.2,<9 do stejné .venv.')
    else:
        print('Vytvořen QR:', cil.name)
