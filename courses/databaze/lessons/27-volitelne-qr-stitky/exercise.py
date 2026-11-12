# Obsah QR zůstává lokální; nic neotevíráme a nikam jej neposíláme.
from qr_podpora import over_qr_text, cil_png, ziskej_qrcode
from soubory import bezpecny_cil

def qr_png(text, cesta, *, zdroj=None):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')
# V Akademii vznikne PNG v dočasném běhu; pro vlastní soubor uložte pracovní složku.
if __name__ == '__main__':
    cil = qr_png('PY-AKADEMIE:PUJ:18', 'stitek.png')
    if cil is None:
        print('QR je volitelný. Doinstalujte qrcode[pil]>=8.2,<9 do stejné .venv.')
    else:
        print('Vytvořen QR:', cil.name)
