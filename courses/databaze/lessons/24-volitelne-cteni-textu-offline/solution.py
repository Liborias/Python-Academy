# Výchozí náhled nevytváří zvuk. Skutečnou řeč musí uživatel zvolit výslovně.
import subprocess
from hlas import vyber_prikaz, over_text

def precti(text, *, mluv=False):
    text = over_text(text)
    if not mluv:
        return 'nahled'
    prikaz = vyber_prikaz()
    if prikaz is None:
        return 'nedostupne'
    try:
        subprocess.run(prikaz, input=text, text=True, encoding='utf-8', check=True,
                       capture_output=True, errors='replace', timeout=15)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return 'nedostupne'
    return 'precteno'
# V Akademii běží pouze textový náhled, bez ovladače řeči a reproduktoru.
if __name__ == '__main__':
    text = 'Ahoj, toto je ukázková poznámka.'
    print('Text:', text)
    print('Režim:', precti(text))
    print('Pro skutečnou offline řeč použijte v uložené složce precti.py --mluv.')
