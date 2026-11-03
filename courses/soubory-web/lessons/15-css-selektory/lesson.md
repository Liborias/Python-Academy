## Zkrácené hledání

Hledat vnořené značky pomocí `find` a `find_all` jednu po druhé je zdlouhavé. Webové stránky mají pro popis „co chci najít“ vlastní jazyk: **CSS selektory**. BeautifulSoup je zná v metodách `select` (všechny nálezy, seznam) a `select_one` (první nález, nebo `None`).

| Selektor | Najde |
|---|---|
| `h3` | všechny značky `h3` |
| `.cena` | značky s třídou `cena` |
| `#p2` | značku s `id="p2"` |
| `div.produkt` | `div` s třídou `produkt` |
| `.produkt h3` | `h3` uvnitř značky s třídou `produkt` (mezera = uvnitř) |
| `a[href]` | odkazy, které mají atribut `href` |

```python
for cena in soup.select(".produkt .cena"):
    print(cena.get_text(strip=True))        # např. "12 Kč"

prvni = soup.select_one("#p2 h3")          # první nález, nebo None
```

Hodnotu z proměnné vložíte do selektoru f-řetězcem: `soup.select_one(f"#{id_} a")` hledá odkaz uvnitř značky s `id` uloženým v proměnné `id_`.

Tečka znamená třídu, křížek `#` identifikátor, mezera „uvnitř“. Selektor píšete tak, jak ho znají tvůrci stránek, a v prohlížeči se dá vyzkoušet (vývojářské nástroje, panel *Elements*).

## Třídy značky

Atribut `class` vrací BeautifulSoup jako **seznam** tříd: pro `<div class="produkt vyprodano">` je `div.get("class")` rovno `["produkt", "vyprodano"]`. Dá se tedy zjistit, jestli v něm třída je: `"vyprodano" in div.get("class", [])`.

## Text s číslem

Cena `12 Kč` je text. Číslo z něj dostanete rozdělením: `"12 Kč".split()[0]` je `"12"` a `int("12")` je `12`.

## Váš úkol

Funkce dostávají HTML jako **text** (soubor `produkty.html` leží vedle programu). Produkty jsou `div` s třídou `produkt`; na stránce je ještě patička, jejíž `.cena` mezi produkty nepatří. V `nazvy`, `ceny` a `odkaz_produktu` použijte `select` nebo `select_one`.

1. `nazvy(html)` vrátí seznam názvů produktů (`h3` uvnitř `.produkt`).
2. `ceny(html)` vrátí seznam cen produktů jako celá čísla (z textu `12 Kč`).
3. `skladem(html)` vrátí názvy produktů, které **nemají** třídu `vyprodano`.
4. `odkaz_produktu(html, id_)` vrátí adresu odkazu v produktu s daným `id`, nebo `None`.
