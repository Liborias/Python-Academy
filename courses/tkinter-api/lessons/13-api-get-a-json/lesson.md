## Okno si připraví data

Na dvě lekce odložíme okno a v konzoli postavíme síťovou část. Později ji připojíme do Tkinteru. API je rozhraní, přes které program požádá jiný program o data. REST API obvykle nabízí adresy pro jednotlivé zdroje a využívá metody HTTP. GET slouží ke čtení: tady požádáme o kurz měny.

Všechna data této části jsou smyšlená pro výuku. EUR má cvičně 25 CZK, USD 20 a GBP 30 za jednu jednotku; datum je pevně 2026-01-15. Nejde o aktuální bankovní kurz. Server běží jen na 127.0.0.1, tedy na stejném počítači, a nepotřebuje internet ani účet.

## Nejprve requests a pomocný soubor

Od této lekce používáme balíček requests. Příprava podkurzu jej instaluje; ve stejné .venv jej lze ověřit příkazem `python -c "import requests; print(requests.__version__)"`. Pokud chybí, ve zvoleném prostředí použijte `python -m pip install requests`. Python musí být stejný jako při spuštění Akademie. Tkinter nyní nic nového instalovat nepotřebuje.

Vedle programu je připravený cvicne_api.py. Zápis `with cvicne_api() as adresa` spustí místní server na volném portu, například http://127.0.0.1:50123, a uloží jeho základní URL do adresa. Po opuštění bloku se server ukončí. Port se může při každém spuštění změnit, proto adresu nezapisujeme natvrdo. Pomocník je součást lekce, nemusíte jej přepisovat. V aplikaci i pracovní složce editoru jej dostanete vedle reseni.py; při ručním kopírování zkopírujte také obsah files.

## Co znamená požadavek

```python
odpoved = requests.get(adresa.rstrip("/") + "/kurz", params={"mena": symbol}, timeout=2)
```

Základní adresa určuje server, cesta /kurz požadovaný zdroj. Rstrip("/") odstraní případné koncové lomítko a zabrání jeho zdvojení. Params vytvoří dotaz, například /kurz?mena=EUR, a správně zakóduje jeho hodnoty. Symbol připravíme pomocí strip().upper(), takže uživatel může zadat i malé písmo a krajní mezery.

Timeout=2 omezuje čekání na připojení a nečinnost při čtení odpovědi. Není to celkový dvousekundový stopky pro celý přenos. Při překročení requests vyvolá výjimku; nekonečné čekání nechceme ani u místního serveru.

Get vrátí Response, tedy odpověď, nikoli hotový slovník. Status_code je stav HTTP. Volání raise_for_status() odmítne chybové stavy 4xx a 5xx výjimkou HTTPError. Samotné get vrátí Response i pro stav 503 a bez tohoto volání výjimku HTTPError automaticky nevyvolá.

Metoda json() rozebere tělo odpovědi na objekty Pythonu. V našem API je to slovník s mena, czk_za_jednotku, datum a zdroj. Syntakticky platný JSON ještě nezaručuje správný tvar ani hodnoty; to přidáme v další lekci.

## Váš úkol

Dokončete nacti_kurz(adresa, mena): normalizujte měnu, použijte předanou adresu, cestu /kurz a parametr mena. Omezte čekání rozumným kladným timeoutem do 3 sekund, ověřte HTTP stav a vraťte celý rozebraný JSON. Chyby zatím nechte vystoupat k volajícímu. Ukázka volá správné EUR/USD, takže doběhne bez chyby.

Spusťte ukázku, porovnejte vrácené měny a vysvětlete rozdíl mezi Response a slovníkem. Potom zkuste GBP. Pro tuto lekci ještě neověřujeme schéma dat a nevytváříme okno: učíme se, co skutečně proběhne mezi požadavkem a odpovědí.
