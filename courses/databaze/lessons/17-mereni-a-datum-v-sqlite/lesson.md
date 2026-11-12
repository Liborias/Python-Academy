## Měření není jen hmotnost

Každý záznam uloží datum, kg, výšku v cm a poznámku. Výšku uchováváme u každého měření, aby se starý výpočet nezměnil po úpravě aktuálního vstupu. BMI do databáze neukládáme: spočítáme ho z původních hodnot. Dva záznamy stejného dne jsou dovoleny a mají různá id.

```python
# ISO zápis má pevné pořadí rok-měsíc-den a funguje i jako řaditelný text.
from datetime import date
print(date.fromisoformat('2024-02-29'))
```

Rok 2024 má 29. únor, 2026 ho nemá. `over_datum` ověří skutečný kalendářní den a přesný tvar RRRR-MM-DD. Zápisy 20260401, 2026-4-1 ani mezery navíc nepřijímáme. Budoucí platná data jsou pro tento cvičný tracker dovolena.

## Co dělají přiložené součásti

`vypocet.py` obsahuje definice z 16, `priprava.py` otevře SQLite s autocommit=False, připraví tabulku a ověří požadované sloupce. Nejde o migraci cizí databáze: používejte nový `bmi.sqlite3`. `over_mereni` ověří datum, kladná konečná čísla, vypočitatelný BMI a text poznámky. Poznámku neořezává: mezery, čeština, apostrof i nový řádek jsou data.

Konstruktor modelu uloží self.con a cestu. Pro paměť je self.cesta None, pro soubor absolutní Path. Model vlastní každou celou transakci. `with self.con` při úspěchu potvrdí INSERT, při výjimce vrátí změny; spojení zavře až close. Nepřidávejte do modelu cizí napůl hotové zápisy přes con.

## Váš úkol

Doplňte **Tracker.pridej** a **Tracker.seznam**. Pridej přijímá `den, hmotnost, vyska_cm, poznamka=''`, zavolá over_mereni a v jedné vlastní transakci vloží hodnoty přes ? parametry. Vrátí skutečné lastrowid. ValueError se předá volajícímu; neplatné měření nesmí vytvořit řádek. Úspěch musí hned vidět i nové spojení, ještě před pozdějším čtením modelem.

Seznam vrátí [(id, datum, kg, cm, poznámka)] seřazené podle data a při shodě podle id. Neřaďte podle českého formátu data ani pouze pořadí vložení. Prázdná DB dává []. Také čtecí metoda může ukončit vlastní transakci modelu. Import nic neotevírá. Close je připravené, opakovatelné a zavřený model se automaticky neobnovuje.

Ukázka vytvoří dočasný soubor, vloží záznam, model zavře a nový model přečte stejnou cestu. Čtení původním spojením by samo nedokázalo potvrdit trvalost. Po skončení se dočasná složka uklidí; vaše vlastní měření nevznikají v této ukázce.
