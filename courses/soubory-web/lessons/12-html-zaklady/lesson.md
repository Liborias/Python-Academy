## Z čeho se skládá webová stránka

Webová stránka je **textový soubor** v jazyce HTML. Prohlížeč ho zobrazí jako stránku. Python si ho může přečíst jako každý jiný text. Soubor `stranka.html` najdete ve složce programu.

HTML se skládá ze **značek** (anglicky *tag*), které text obalují:

```html
<h1>Zvířata v ZOO</h1>
<p class="info">Otevřeno denně od 9 do 17 hodin.</p>
<a href="mapa.html">Mapa ZOO</a>
```

- Značka má **začátek** `<p>` a **konec** `</p>` (s lomítkem). Mezi nimi je obsah.
- Do začátku značky se píšou **atributy** ve tvaru `jmeno="hodnota"`: `class`, `id`, `href` (adresa odkazu).
- Značky se **vnořují**: seznam `<ul>` obsahuje položky `<li>`.

| Značka | Význam |
|---|---|
| `<h1>` až `<h6>` | nadpisy |
| `<p>` | odstavec |
| `<a href="...">` | odkaz |
| `<ul>`, `<li>` | seznam a položka seznamu |
| `<table>`, `<tr>`, `<td>` | tabulka, řádek, buňka |
| `<div>`, `<span>` | obecné obaly |

## Hledání v textu

Metoda `text.find(co)` vrátí pozici prvního výskytu textu `co`, a pokud tam není, číslo `-1`. Druhý parametr říká, **odkud** hledat: `text.find("</h1>", 5)`. Spolu s řezem textu se tak dá vytáhnout část mezi značkami:

```python
zacatek = html.find("<h1>") + len("<h1>")
konec = html.find("</h1>")
nadpis = html[zacatek:konec]
```

Metoda `text.count(co)` spočítá, kolikrát se text vyskytuje.

Takové ruční hledání funguje u jednoduchých případů, ale u skutečných stránek je křehké: stačí přidat atribut nebo mezeru a kód se rozbije. Proto existují nástroje, které HTML **chápou**. Příští lekce ukáže `BeautifulSoup`. Teď si hledání vyzkoušíte jako motivaci.

## Váš úkol

Funkce dostávají HTML jako **text**. Značky v testech mají vždy přesně tvar `<h1>`, `<li>` a `<a href="...">` s dvojitými uvozovkami.

1. `nadpis(html)` vrátí text mezi `<h1>` a `</h1>`, nebo prázdný řetězec, pokud tam nadpis není.
2. `pocet_polozek(html)` vrátí počet položek seznamu `<li>`.
3. `odkazy(html)` vrátí seznam adres z atributů `href="..."` v pořadí, jak jsou v textu. Pro text bez odkazů vrátí prázdný seznam.
