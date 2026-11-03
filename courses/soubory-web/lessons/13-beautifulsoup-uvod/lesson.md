## Nástroj, který rozumí HTML

Ruční hledání v textu je křehké. **BeautifulSoup** HTML přečte, pochopí strukturu značek a umožní se ptát: „dej mi nadpis“, „najdi odkaz“. Je to knihovna, kterou je nutné nainstalovat (`beautifulsoup4`). Pokud jste postupovali podle návodu na přípravu prostředí, už ji máte.

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
```

První parametr je HTML jako **text**, druhý říká, kterým způsobem se má text rozebrat (`"html.parser"` je součástí Pythonu).

## Hledání prvního výskytu

```python
nadpis = soup.find("h1")             # první značka <h1>, nebo None
print(nadpis.get_text())             # text uvnitř značky
```

- `soup.find("p")` vrátí **první** nalezenou značku `p`. Pokud takové není, vrátí `None`. Před použitím výsledku je proto dobré ověřit `if nalezeno:`, jinak by `None.get_text()` skončilo chybou.
- `znacka.get_text()` vrátí text uvnitř, `get_text(strip=True)` navíc odstraní mezery a zalomení na okrajích.
- Hledat se dá i podle atributů: `soup.find("p", id="uvod")` a `soup.find("p", class_="info")`. Pozor, parametr se jmenuje `class_` s podtržítkem, protože `class` je v Pythonu vyhrazené slovo.

## Atributy značky

Atributy se čtou stejně jako klíče slovníku:

```python
odkaz = soup.find("a")
odkaz["href"]              # adresa, ale KeyError, když atribut chybí
odkaz.get("href")          # adresa, nebo None, když atribut chybí
```

## Váš úkol

Funkce dostávají HTML jako **text** (soubor `stranka.html` leží vedle programu).

1. `nadpis(html)` vrátí text prvního `<h1>` (bez mezer na okrajích), nebo `None`, pokud tam není.
2. `prvni_odstavec(html)` vrátí text prvního `<p>`, nebo `None`.
3. `prvni_odkaz(html)` vrátí dvojici `(text odkazu, adresa)` prvního odkazu `<a>`. Pokud odkaz nemá `href`, použije se jako adresa `None`. Pokud žádný odkaz není, vrátí `None`.
4. `text_s_id(html, id_)` vrátí text značky s daným `id`, nebo `None`.
5. `text_s_tridou(html, trida)` vrátí text první značky s danou třídou, nebo `None`.

Používejte `BeautifulSoup`. Pozor na prázdný výsledek `find`.
