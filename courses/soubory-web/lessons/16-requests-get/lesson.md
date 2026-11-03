## Počítač se ptá serveru

Webová stránka je jen **text**, který vám pošle jiný počítač (server). Váš prohlížeč se zeptá: „pošli mi stránku `/knihy.html`“ a server odpoví. Tomuto dialogu se říká **HTTP**. Program se může ptát úplně stejně, k tomu slouží balíček `requests`.

```python
import requests

odpoved = requests.get("http://127.0.0.1:8000/index.html")
print(odpoved.status_code)      # 200
print(odpoved.text)             # text stránky
```

`requests.get(adresa)` pošle dotaz a vrátí objekt s odpovědí. Nejdůležitější je na něm:

| Co | Význam |
|---|---|
| `odpoved.status_code` | číselný výsledek: `200` v pořádku, `404` stránka neexistuje, `500` chyba serveru |
| `odpoved.text` | obsah odpovědi jako text |
| `odpoved.headers` | hlavičky, například `headers["content-type"]` říká, o jaká data jde |
| `odpoved.json()` | obsah ve formátu JSON rovnou přeložený na slovník nebo seznam |

## Proč zde používáme „vlastní server“

V lekcích se nestahují skutečné weby: zatěžovalo by je to a lekce by přestaly fungovat při výpadku internetu nebo změně stránky. Soubor `dilna_web.py` (je u lekce) proto spustí **malý server na vašem počítači**:

```python
from dilna_web import spust

adresa = spust()                 # například "http://127.0.0.1:50321"
odpoved = requests.get(adresa + "/index.html")
```

Adresa `127.0.0.1` vždy znamená „tento počítač“, číslo za dvojtečkou (port) se pokaždé zvolí volné. Server vydává soubory ze složky `web`, která leží vedle vašeho programu. Pro `requests` je to stejné jako skutečný web, takže všechno, co se naučíte, použijete i na internetu.

Server umí i pár zvláštních adres, například `/_status/404` odpoví chybou 404 (využijeme je v dalších lekcích).

## Stránka a data

Text stránky je HTML, a tak ho můžete rovnou předat BeautifulSoup z minulých lekcí:

```python
soup = BeautifulSoup(odpoved.text, "html.parser")
```

Pro data ve formátu JSON je tu zkratka `odpoved.json()`, nemusíte volat `json.loads`.