## Co už umíte

| Téma | Nejdůležitější |
|---|---|
| Soubory | `with open(cesta, "r", encoding="utf-8")`, režimy `r`, `w`, `a`, `wb` |
| Cesty | `Path(...)`, `/`, `exists`, `glob`, `mkdir(exist_ok=True)` |
| Chyby | `try` / `except FileNotFoundError`, `OSError` |
| CSV | `csv.DictReader`, `DictWriter`, `newline=""`, hodnoty jsou vždy text |
| JSON | `json.load`, `json.dump(..., ensure_ascii=False, indent=2)` |
| HTML | `BeautifulSoup`, `find`, `find_all`, `select`, `get_text(strip=True)`, `get` |
| Web | `requests.get(url, timeout=...)`, `raise_for_status`, `RequestException`, `urljoin` |
| Slušnost | `robots.txt`, `User-Agent`, pauzy mezi dotazy |

## Úkol

Čtyři malé funkce, každá z jiné oblasti. Soubor `body.csv` je u lekce:

```
jmeno,trida,body
Eva,7.A,42
...
```

Při chybějícím souboru vracejte prázdný výsledek místo pádu programu.