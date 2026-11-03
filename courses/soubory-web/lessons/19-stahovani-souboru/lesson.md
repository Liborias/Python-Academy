## Text a bajty

Dosud jste stahovali text (`odpoved.text`). Obrázek, PDF nebo zip ale text nejsou, jsou to **bajty**. Pro ně má odpověď atribut `odpoved.content` a soubor se musí zapisovat v **binárním režimu** `"wb"` (write binary), který žádné kódování nepoužívá:

```python
odpoved = requests.get(url, timeout=5)
odpoved.raise_for_status()
with open("obrazek.png", "wb") as soubor:
    soubor.write(odpoved.content)
```

Soubor zapisujte až po úspěšném stažení (po `raise_for_status`), jinak vznikne poškozený nebo prázdný soubor.

## Adresy na stránce: urljoin

Obrázky na stránce mají adresy v různých podobách:

| Zápis v HTML | Význam |
|---|---|
| `img/a.png` | relativně ke stránce, kde je odkaz |
| `/img/b.png` | od začátku webu |
| `https://jiny.cz/c.png` | úplná adresa |

Z libovolné z nich uděláte úplnou adresu funkcí `urljoin` ze standardní knihovny:

```python
from urllib.parse import urljoin

urljoin("http://127.0.0.1:8000/galerie.html", "img/a.png")    # http://127.0.0.1:8000/img/a.png
urljoin("http://127.0.0.1:8000/galerie.html", "/img/b.png")   # http://127.0.0.1:8000/img/b.png
```

## Jméno souboru z adresy

Poslední část adresy je jméno souboru: `adresa.rsplit("/", 1)[1]` z `.../img/a.png` dá `a.png`.

## Složka pro stažené soubory

`Path(slozka).mkdir(exist_ok=True)` složku vytvoří, a pokud už existuje, nehlásí chybu. Cestu k souboru ve složce skládejte lomítkem: `Path(slozka) / "a.png"`.