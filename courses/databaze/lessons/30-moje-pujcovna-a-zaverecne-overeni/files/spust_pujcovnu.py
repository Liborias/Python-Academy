from reseni import MojePujcovna
from predani import cesty_projektu,zaloha_projektu
from qr_export import qr_png
from ovladani import konzole

if __name__ == '__main__':
    konzole(MojePujcovna,__file__,cesty_projektu,zaloha_projektu,qr_png,final=True)
