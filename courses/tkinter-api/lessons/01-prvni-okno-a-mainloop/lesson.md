## Program dostane vlastní okno

V tomto podkurzu vytvoříme okenní nástroje, později je propojíme s HTTP API a e-maily. Začneme samotným oknem. První čtyři lekce používají standardní knihovnu Pythonu a Tkinter; requests přijde až v části o API. Znalost funkcí, podmínek a řetězců ze Základů zatím stačí.

Tkinter je rozhraní Pythonu ke knihovně Tk, která vytváří skutečná okna operačního systému. Kód nespouští okno uvnitř webové stránky. Otevře je na počítači, kde běží Python a server Akademie. Při práci na vzdáleném serveru potřebuje tento počítač také grafickou plochu. Na běžném místním počítači můžete mít prohlížeč i okno vedle sebe.

## Nejprve ověřte prostředí

Před lekcemi otevřete přípravu tohoto podkurzu a vyberte svůj systém a editor. Python z projektové .venv ověřte v terminálu ve složce Akademie:

```text
Windows PowerShell: .\.venv\Scripts\python.exe -m tkinter
macOS/Linux: ./.venv/bin/python -m tkinter
```

Vyberte příslušný příkaz, ne oba. -m tkinter spustí vestavěnou zkušební aplikaci. Pokud se objeví malé okno s verzí Tk, prostředí funguje. Zavřete je před pokračováním. V editoru zvolte stejný interpreter z .venv.

Tkinter se neinstaluje příkazem pip install tkinter. Ve Windows bývá součástí instalace Pythonu z python.org. Na Linuxu může chybět odpovídající systémový balíček python3-tk; Homebrew používá odpovídající python-tk, například python-tk@3.14. Rozhodující je ověření stejným Pythonem, kterým projekt spouštíte. Chyba o chybějící grafické ploše neznamená chybějící pip balíček.

## Co provedou jednotlivé řádky

import tkinter as tk načte modul a dá mu krátké jméno tk. Volání tk.Tk() vytvoří hlavní okno a vrátí objekt, který si uložíme do proměnné okno. Tečka potom volá jeho metody:

- title("Moje první okno") nastaví text v záhlaví okna.
- geometry("420x240") nastaví počáteční šířku 420 a výšku 240 pixelů. Píše se malé písmeno x uvnitř textu, nikoli znak násobení.
- minsize(320, 180) omezí zmenšení okna: šířka i výška jsou tentokrát samostatná čísla.

Proměnná může mít i jiné jméno. Důležité je, aby metody pracovaly se stejným hlavním oknem.

## Proč program čeká v mainloop

mainloop() spustí hlavní smyčku událostí Tk. Ta čeká na kliknutí, změnu rozměrů nebo zavření okna a předává je příslušným částem programu. Okno během čekání zůstává ovladatelné. Nepíšeme vlastní while True ani sleep, které by mu bránily zpracovávat události.

Při zavření okna smyčka skončí. V Akademii tedy běh ukázky trvá, dokud okno nezavřete nebo nepoužijete Stop. Prázdné okno v této lekci je zamýšlený výsledek; popisky přidáme příště.

## Váš úkol

Vytvořte jedno viditelné hlavní okno s titulkem Moje první okno, počáteční velikostí 420x240 a nejmenšími rozměry 320x180. Nakonec spusťte právě jednu hlavní smyčku. Další ovládací prvky zatím nejsou potřeba.

Spusťte ukázku a zkuste okno zmenšit i zvětšit. Potom je zavřete a vytvořte vlastní řešení. Tlačítko Zkontrolovat ověří nastavení; skutečné umístění a vzhled si prohlédněte v otevřeném okně. Stejný soubor lze spustit v editoru nebo příkazem python reseni.py v pracovní složce lekce.
