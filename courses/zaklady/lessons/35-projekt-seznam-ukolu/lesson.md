## Příkazy z klávesnice

Poslední z menších projektů je program, který udržuje seznam úkolů. Hráč zadává **příkazy**:

```text
pridej Koupit mléko
pridej Napsat úkol
hotovo 1
seznam
```

Úkol je slovník `{"text": "Koupit mléko", "hotovo": False}` a všechny úkoly leží v seznamu. Využijete seznam slovníků z lekce 21.

## Rozdělení příkazu

Příkaz má dvě části: slovo a zbytek. Metoda `split` s druhým parametrem rozdělí text nejvýš na tolik částí:

```python
"pridej Koupit mléko".split(" ", 1)    # ["pridej", "Koupit mléko"]
"seznam".split(" ", 1)                 # ["seznam"]
```

Pokud je výsledek kratší, nemá příkaz žádný zbytek. Rozbalit na dvě proměnné se proto dá až po kontrole délky `len(casti)`.

## Číslování a zkrácený if

Při výpisu se hodí číslovat řádky od 1. Pomůže `enumerate(seznam, 1)`, který vrací dvojice (číslo, prvek):

```python
for cislo, ukol in enumerate(ukoly, 1):
    print(cislo, ukol["text"])
```

Krátké rozhodnutí se dá zapsat do jednoho řádku: `znacka = "x" if ukol["hotovo"] else " "` znamená „`x`, pokud je hotovo, jinak mezera“.

## Váš úkol

1. `pridej_ukol(ukoly, text)` přidá nový úkol (`hotovo` je `False`) na konec seznamu a seznam vrátí.
2. `dokonc_ukol(ukoly, cislo)` označí úkol číslo `cislo` za hotový (číslují se od **1**) a vrátí `True`. Pokud takové číslo neexistuje (0, záporné, příliš velké), nic nezmění a vrátí `False`.
3. `procento_hotovo(ukoly)` vrátí, kolik procent úkolů je hotových (bez zaokrouhlení). Prázdný seznam dává `0`.
4. `zpracuj_prikaz(ukoly, prikaz)` provede příkaz a **vrátí text odpovědi**:
   - `pridej <text>` přidá úkol a vrátí `Přidáno: <text>`,
   - `hotovo <číslo>` dokončí úkol a vrátí `Hotovo: <text úkolu>`, při neplatném čísle (i když není číslo) vrátí `Neplatné číslo.`,
   - `seznam` vrátí řádky `1. [ ] Koupit mléko` (hotový úkol má `[x]`) spojené znakem nového řádku `\n`, pro prázdný seznam text `Žádné úkoly.`,
   - cokoli jiného vrátí `Neznámý příkaz.`
5. `hlavni_smycka(ukoly)` čte příkazy pomocí `input("> ")`, vypisuje odpovědi a skončí na příkazu `konec`.
