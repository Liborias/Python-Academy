from reseni import zabal_text,rozbal_text
from sezeni import Ucty,Sezeni
from ovladani import konzole
from prenos import prenos

if __name__ == '__main__':
    def proved(akce,sezeni,cesta):
        return prenos(akce,sezeni,cesta,zabal_text,rozbal_text)
    konzole(Ucty,Sezeni,__file__,proved)
