# Výchozí náhled nevytváří zvuk. Skutečnou řeč musí uživatel zvolit výslovně.
import subprocess
from hlas import vyber_prikaz, over_text

def precti(text, *, mluv=False):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')
# V Akademii běží pouze textový náhled, bez ovladače řeči a reproduktoru.
if __name__ == '__main__':
    text = 'Ahoj, toto je ukázková poznámka.'
    print('Text:', text)
    print('Režim:', precti(text))
    print('Pro skutečnou offline řeč použijte v uložené složce precti.py --mluv.')
