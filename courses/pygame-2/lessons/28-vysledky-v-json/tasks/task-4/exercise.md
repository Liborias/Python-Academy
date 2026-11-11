## Čtení verzovaného JSON

Vytvořte **nacti_vysledky(cesta)**. Čtěte UTF-8 JSON tvaru {'verze': 1, 'vysledky': [...]} a vraťte připravenou vyber_vysledky nad seznamem. Verze je přesně int 1, True neplatí. Neplatný kořen/verze/seznam, chybějící soubor, rozbitý JSON a neplatné UTF-8 vrátí [].

Použijte úzké zachycení FileNotFoundError, json.JSONDecodeError a UnicodeDecodeError. Jiný OSError (například zadaný adresář či odepřený přístup) má projít volajícímu, aby jej mohl oznámit. Čtení nesmí soubor měnit ani automaticky přepisovat poškozený obsah.
