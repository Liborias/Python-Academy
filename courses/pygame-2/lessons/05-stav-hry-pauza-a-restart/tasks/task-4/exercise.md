### Menu, hra, pauza a konec

`Rezimy()` má stav='menu'. KEYDOWN Enter změní menu→hra. KEYDOWN Escape mění hra↔pauza; v menu ani v konec nic neudělá. QUIT změní libovolný stav na konec. Ostatní události/klávesy nic nemění, ze stavu konec se klávesami nevracíme. Metoda se jmenuje zpracuj(udalost). Stavový automat znamená, že stejný vstup může podle aktuálního stavu udělat jinou věc.
