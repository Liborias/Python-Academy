import re
from dilna_check import check

c = check()
r = c.tk_run()
if c.tk_no_error(r):
    roots = r.widgets('root')
    c.add('Jedno viditelné hlavní okno', len(roots) == 1 and roots[0]['visible'], 'Vytvořte jedno okno pomocí Tk a ponechte je zobrazené.')
    c.add('Jedna hlavní smyčka', r.mainloops == 1, 'Na konec přidejte mainloop(), nepoužívejte vlastní nekonečný cyklus.')
    if len(roots) == 1:
        root = roots[0]
        c.add('Titulek okna', root['title'] == 'Moje první okno', 'Použijte title s textem Moje první okno.')
        c.add('Počáteční velikost 420 × 240', bool(re.fullmatch(r'420x240(?:[+-]\d+[+-]\d+)?', root['geometry'])), 'Geometry očekává text 420x240, pořadí je šířka a výška.')
        c.add('Nejmenší velikost 320 × 180', root['minsize'] == [320, 180], 'Minsize přijímá dvě čísla: 320 a 180.')
c.done()
