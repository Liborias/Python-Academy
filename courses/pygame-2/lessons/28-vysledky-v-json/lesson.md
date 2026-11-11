## Hra si pamatuje dokončené pokusy

JSON je textový formát vhodný pro jednoduché výsledky. Slovník bude mít verze=1 a vysledky jako seznam záznamů jmeno/body/uspech. Verze umožní později změnit formát bez tichého chybného výkladu starých dat.

```python
import json
zaznam = {'jmeno': 'Žofie', 'body': 7, 'uspech': True}
text = json.dumps(zaznam, ensure_ascii=False)
print(text)
print(json.loads(text) == zaznam)
print('Bool je také int:', isinstance(True, int))
```

JSON používá true, Python True; json je převádí. Poslední řádek vypíše True a vysvětluje, proč počet bodů musíme ověřit přísněji než přes isinstance(..., int). Načtená data nepovažujeme automaticky za správná.

## Pět malých odpovědností

Úkoly postupně ověří jeden záznam, vytvoří čisté kopie, seřadí pořadí, načtou soubor a bezpečně nahradí starší výsledek. Potřebné dřívější funkce jsou hotové ve vysledky_podklady.py, každý úkol je možné řešit samostatně.

Prázdné výsledky při prvním spuštění jsou běžný stav. Chybějící soubor, neplatný JSON a chyba přístupu ale nejsou stejná událost. Poškozený soubor při čtení nepřepisujeme; lze se k němu vrátit při opravě. Odepřený přístup má dostat volající jako OSError, aby zobrazil srozumitelnou zprávu.

## Zápis má proběhnout celý

Otevřít cíl v režimu w by ho hned vyprázdnilo. Proto nejprve zapíšeme do jedinečného souboru vedle něj, soubor uzavřeme a teprve potom os.replace vymění jméno za hotový obsah. Finally uklidí dočasný soubor i při chybě. Před uzavřením na Windows nenahrazujeme. Tento jednoduchý postup není databáze pro více současných hráčů.

Ukázky pracují v dočasných složkách; po ukončení je uklidí. Vaše skutečné výsledky zatím nemění. Poslední projekt předá funkci vlastní cestu pro trvalejší ukládání.

## Váš úkol

Vytvořte **platny_vysledek(zaznam)** vracející výhradně True/False. Platný je slovník s jmeno (str, po strip 1–24 znaků), body (přesně int, nezáporný) a uspech (přesně bool). Další klíče nevadí. Vstup se nemění.

V Pythonu je bool potomkem int: isinstance(True, int) vrací True. Proto počet dat ověřte přes type(hodnota) is int. Úspěch zase nepatří do stejného pole jako body; neúspěšná mise může mít více dat než úspěšná.
