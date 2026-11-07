## Malý nástroj ze známých částí

Spojíme rámeček, vstup, přepínače, tlačítko a Enter do převodníku vzdálenosti. Kilometry násobíme 1000, metry dělíme 1000. Zápornou vzdálenost v tomto nástroji nepovolujeme. Nula je platná. Chybný text nesmí okno ukončit: uživatel dostane zprávu a může se opravit.

Nová je hlavně dělba práce. Samostatná funkce `preved_vzdalenost(hodnota, smer)` dostane číslo a směr km-m nebo m-km, vrátí číslo a nepracuje s žádným widgetem. Funkce tlačítka přečte text z formuláře, zavolá výpočet a výsledek zobrazí. Výpočet tak půjde používat i v konzoli a ověřovat bez okna.

## Číslo není totéž co text ve vstupu

```python
hodnota = float(vstup.get().strip().replace(",", "."))
```

Get vrátí text. Strip odstraní krajní mezery, replace nahradí desetinnou čárku tečkou a float převede například 1.25 na číslo. Povolujeme tedy 1,25 i 1.25, bez oddělovačů tisíců. Text jako abc, prázdné pole, několik teček nebo smíchaná čárka s tečkou vyvolá ValueError. Mezery uvnitř čísla neodstraňujeme.

Také float("nan") nebo float("inf") jsou pro Python platné zápisy speciálních čísel: neurčené hodnoty a nekonečna. Pro vzdálenost nejsou vhodné. Po `import math` ověří `math.isfinite(hodnota)`, že je číslo konečné. Vrací True/False. Ve výpočtu odmítneme nekonečné či záporné číslo pomocí ValueError a ověříme i konečnost výsledku: i konečný obrovský vstup může při násobení přetéct.

## Chyba se zpracuje na hranici formuláře

Výpočet pro neplatné číslo nebo neznámý směr vyvolá ValueError. V callbacku obalíme převod textu a volání výpočtu do try/except ValueError. Chybu zobrazíme v původním výsledném popisku a `return` ukončí tento jeden callback. Neukončuje mainloop ani celou aplikaci. Další kliknutí nebo Enter znovu přečte aktuální vstup.

Úspěšný výsledek formátujeme jako `f"{cislo:.3f} {jednotka}"`. `.3f` znamená běžný desetinný zápis s přesně třemi místy a zaokrouhlením pro zobrazení. Například 1,25 km dá 1250.000 m a 1250 m dá 1.250 km. Samotná výpočetní funkce nic nezaokrouhluje ani nepřidává jednotku. Python používá ve výstupu tečku; vstupní čárku jsme přijali vlastní úpravou textu.

## Okno vznikne až při spuštění

Vytvoření okna je přesunuté do funkce hlavni. Vnořený callback má přístup k widgetům této funkce. Základy funkcí se nemění: jména hledá také v obklopující funkci. Modulová funkce preved_vzdalenost k těmto lokálním widgetům nepřistupuje.

```python
if __name__ == "__main__":
    hlavni()
```

Při přímém spuštění souboru je __name__ rovno "__main__" a okno se vytvoří. Při importu ze souboru jej Python pojmenuje podle modulu a tento blok přeskočí. Lze pak importovat výpočet bez otevření okna. Importy samotných tkinter/ttk okno nevytvářejí; rozhodující je až Tk().

## Váš úkol

Dokončete dvě připravené funkce. `preved_vzdalenost(hodnota, smer)` přijímá konečné nezáporné číslo int/float a směr km-m nebo m-km, vrací číselný výsledek. Pro záporné číslo, NaN, nekonečno, přetečení výsledku či neznámý směr vyvolá ValueError. Samotná funkce nesmí otevřít okno, číst vstup ani zobrazovat zprávy.

Callback preved přečte aktuální text, přijme desetinnou tečku i čárku a použije výpočet. Při chybě nastaví přesně Zadejte platné nezáporné číslo. Při úspěchu zobrazí číslo na tři desetinná místa a správnou jednotku, oddělenou mezerou. Ponechte počáteční zprávu Zadejte nezápornou vzdálenost., výchozí směr Kilometry na metry a ovládání tlačítkem Převést i Enterem. Pouhé přepnutí směru výsledek nezmění, další potvrzení použije novou volbu. Obsah Entry při převodu zachovejte.

Připravené rozložení ani hlavní blok není nutné měnit. Vyzkoušejte 1,25 km, 1250 m, nulu, prázdné pole, -1, abc a inf. Po chybě napište nové platné číslo a pokračujte ve stejném okně. Přesvědčte se také, že import funkce v jiném programu žádné okno neotevře.
