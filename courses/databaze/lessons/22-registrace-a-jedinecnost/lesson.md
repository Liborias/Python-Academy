## Jedinečnost hlídá databáze

Účet má id, sjednocené jméno a textový JSON ověřovacího záznamu. Původní heslo se do DB nedostane. `hesla.py` přebírá definice z 21, `priprava.py` vytváří tabulky a vynucuje vazby.

```python
# Casefold pracuje i s Unicode; nespoléháme na ASCII NOCASE v SQLite.
print('  ŽOFIE  '.strip().casefold())
```

Jméno tedy bude žofie. Sjednocujeme pouze jméno, nikoli heslo. Po sjednocení musí mít 1–64 znaků. Uživatel si tak nezaloží duplicitní účet jen změnou velikosti písmen či krajních mezer.

## Proč nestačí nejprve SELECT

Dva běhy by mohly současně zjistit, že jméno ještě neexistuje. UNIQUE u sloupce jmeno je konečné pravidlo. INSERT s parametry buď uloží nový účet, nebo vyvolá IntegrityError. Starý záznam nepřepisujeme a chybu nezamlčujeme jako úspěch.

Scrypt provedeme před krátkou zapisovací transakcí. `with self.con` potvrdí úspěch, vrátí chybu a spojení nezavře. Model vlastní celé spojení; nedávejte do jeho con cizí napůl hotové změny. Tabulka poznámek už připravuje další lekci, přihlašování teprve doplníme.

## Váš úkol

Doplňte **Ucty.registruj(jmeno, heslo)** a **Ucty.seznam()**. Konstruktor otevře vlastní spojení a uloží absolutní self.cesta, pro :memory: None. Schéma má uzivatele(id,jmeno UNIQUE,overeni) a poznamky(id,uzivatel_id,text). Pro projekt použijte nový ucty.sqlite3; CREATE IF NOT EXISTS není migrace jiné DB.

Registruj sjednotí jméno přes jmeno_uctu, vytvoří ověřovací záznam, převede jej json.dumps na text a v jedné transakci vloží přes ? parametry. Vrátí skutečné lastrowid. Neplatné jméno/heslo předá jako ValueError, duplicitu jako IntegrityError. JSON obsahuje jen profil/sůl/otisk, nikdy heslo. Po úspěchu musí účet hned vidět druhé spojení.

Seznam vrátí [(id, jméno)] v pořadí id, bez JSON/hesel. Prázdná DB dává []. Close je opakovatelné, zavřený model se automaticky neobnovuje. Hlavní ukázka vytvoří dočasný soubor, zavře ho a nový model účet znovu přečte. Import neotevírá DB.
