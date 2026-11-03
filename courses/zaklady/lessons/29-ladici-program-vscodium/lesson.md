## Program krok za krokem

Výpisy `print` fungují, ale po čase jich je moc. Ladicí program (**debugger**) umí program zastavit na vybraném řádku a pak ho spouštět **po jednom řádku**, přičemž ukazuje hodnoty všech proměnných. Ve VSCodium ho zajišťuje rozšíření `ms-python.debugpy`.

> Tato lekce se dělá mimo prohlížeč, přímo ve VSCodium. Kontrola v aplikaci pak jen ověří výsledek vašich oprav.

## Postup ve VSCodium

1. Otevřete soubor s kódem (tlačítko „Otevřít ve VSCodium“, nebo přes **Soubor, Otevřít složku**).
2. Klikněte vlevo vedle čísla řádku. Objeví se červená tečka: **bod přerušení** (breakpoint). Program se na tomto řádku zastaví.
3. Stiskněte **F5** (Spustit ladění). Pokud se zeptá na konfiguraci, vyberte „Ladit aktuální soubor“.
4. Program se zastaví na červené tečce. V levém panelu **Proměnné** (Variables) vidíte aktuální hodnoty.
5. Procházejte program klávesami:

| Klávesa | Význam |
|---|---|
| **F10** | provést řádek a jít na další (volanou funkci přeskočí) |
| **F11** | vstoupit do volané funkce |
| **Shift+F11** | dokončit funkci a vrátit se zpět |
| **F5** | pokračovat do dalšího bodu přerušení |
| **Shift+F5** | ladění ukončit |

6. Do panelu **Sledování** (Watch) můžete napsat výraz, třeba `cisla[-1] + cisla[-2]`, a vidět jeho hodnotu v každém kroku.

## Co sledovat

U cyklu hledejte první řádek, na kterém se hodnota proměnné liší od toho, co jste čekali. Právě tam je chyba, nebo těsně před ním.

## Když F5 nejde

Ladění je jedna z věcí, která se na různých počítačích může chovat různě. Zkuste `docs/reseni-problemu.md`. Záložní řešení funguje všude: do kódu napište `breakpoint()` a spusťte soubor v terminálu. Program se zastaví v jednoduchém ladicím programu `pdb`, kde stačí zadat `p promenna` (vypsat), `n` (další řádek), `c` (pokračovat) a `q` (konec).

## Váš úkol

V editoru jsou tři funkce s chybou. Najděte ji pomocí ladicího programu a opravte.

1. `fibonacci(n)` vrátí seznam prvních `n` Fibonacciho čísel (pro `n` alespoň 2): `0, 1, 1, 2, 3, 5, ...`. Každé další číslo je součet dvou předchozích.
2. `nejdelsi_slovo(veta)` vrátí nejdelší slovo věty. Při shodě první z nich.
3. `pocet_vyskytu(seznam, hodnota)` vrátí, kolikrát se hodnota v seznamu vyskytuje.
