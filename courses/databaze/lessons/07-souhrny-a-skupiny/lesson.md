## Řádky proměníme v přehled

Skladníka často zajímá počet pomůcek, celkové dostupné množství či rozložení podle kategorií. Agregační funkce shrnou více řádků: COUNT počítá, SUM sčítá, MIN/MAX hledají meze a AVG průměr.

```python
import sqlite3
from contextlib import closing
with closing(sqlite3.connect(':memory:', autocommit=True)) as con:
    con.execute('CREATE TABLE sklad (kusy INTEGER)')
    con.executemany('INSERT INTO sklad VALUES (?)', [(0,), (2,)])
    print(con.execute('SELECT COUNT(*), SUM(kusy), AVG(kusy) FROM sklad').fetchone())
```

Výsledek (2, 2, 1.0) zahrnuje i nulu. U prázdné tabulky COUNT vrátí 0, ostatní běžné agregace NULL. Kde dává smysl prázdný součet 0, použijeme COALESCE; prázdné minimum či průměr necháme jako None.

## COUNT sloupce a skupiny

COUNT(*) počítá řádky. COUNT(poznamka) jen hodnoty jiné než NULL, včetně prázdného textu. COUNT(DISTINCT poznamka) počítá různé vyplněné hodnoty. Tyto tři počty nemusí být stejné.

GROUP BY rozdělí řádky do skupin. V této cvičné variantě má pomucky navíc textový sloupec kategorie; v lekci 8 jej nahradíme skutečným odkazem do jiné tabulky. NULL vytvoří jednu společnou skupinu, nespojujte ji předčasně s prázdným názvem.

WHERE vybírá řádky před seskupením, HAVING vybírá už vypočtené skupiny. Podmínka na součet tedy patří až do HAVING. Neseskupené sloupce v přehledu nevybíráme náhodně; SQLite by některé zápisy dovolil, ale jejich význam by byl nejasný.

Výsledné pořadí zadejte výslovně. Pracujeme se standardním row_factory=None a základním řazením SQLite, ne českým slovníkovým. Data i transakci vlastní volající.

## Váš úkol

Vytvořte **celkovy_souhrn(con)**. Z pomucky vrátí jednu n-tici (počet_řádků, součet_kusů, minimum, maximum). Součet prázdné tabulky nahraďte nulou, minimum a maximum zůstanou None. Pro prázdný sklad tedy (0, 0, None, None).

Kusy jsou neprázdná celá čísla z cvičného skladu. COUNT(*) počítá řádky, SUM/MIN/MAX pracují s hodnotami. Spojení a transakci vlastní volající, neukončujte je.
