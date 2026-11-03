## Celé řešení najednou

V tomto projektu spojíte všechno: stáhnete stránku, vytáhnete z ní data a uložíte je do tabulky. Stránka `knihy.html` je nabídka knihkupectví:

```html
<li class="kniha vyprodano">
  <span class="nazev">Půlnoční vlak</span>
  <span class="autor">Petr Dvořák</span>
  <span class="cena">329 Kč</span>
</li>
```

Třída `vyprodano` znamená, že kniha není skladem. Pozor, v patičce stránky je ještě jedna `cena` (poštovné), která mezi knihy nepatří.

## Tři kroky, tři funkce

Dobrý program se dělí na malé části, které jdou zkoušet zvlášť:

1. `ziskej_knihy(html)` převede text stránky na seznam slovníků (nic nestahuje a nic neukládá);
2. `uloz_csv(knihy, nazev)` zapíše seznam do souboru CSV;
3. `stahni_knihy(url, nazev_csv)` obě části spojí: stáhne, zpracuje, uloží.

Hotový soubor `knihy.csv` pak můžete otevřít v tabulkovém procesoru.

## Požadavky

- `cena` je celé číslo (z `"249 Kč"` uděláte `249`);
- `skladem` je `True` nebo `False`, do CSV se zapíše jako `ano` nebo `ne`;
- sloupce v CSV jdou za sebou `nazev`, `autor`, `cena`, `skladem`;
- při chybě stahování funkce `stahni_knihy` vrátí `0` a **žádný soubor nevytvoří**.

Připomenutí: CSV se otevírá s `newline=""` a `encoding="utf-8"`.