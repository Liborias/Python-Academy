## Telefonní seznam v souboru

Poslední projekt modulu spojí práci se soubory, JSON, funkce, slovníky a chyby. Kontakty jsou uložené v souboru `kontakty.json` jako **seznam slovníků**:

```json
[
  {"jmeno": "Eva Nováková", "telefon": "777111222", "email": "eva@example.com"},
  {"jmeno": "Petr Svoboda", "telefon": "602333444", "email": ""}
]
```

Vzorový soubor `kontakty.json` je ve složce programu.

## Návrh

Soubor je jediné místo, kde kontakty žijí. Každá funkce si je načte, případně změní a **uloží zpět**. Společné načtení a uložení proto napíšete jednou a ostatní funkce je využijí. Je to stejný nápad jako u deníku.

Pozor na chybějící soubor: při prvním spuštění programu ještě neexistuje, a to není chyba, jen prázdný seznam kontaktů.

## Váš úkol

Všechny funkce dostávají jako první parametr jméno souboru.

1. `nacti_kontakty(nazev)` vrátí seznam kontaktů. Pokud soubor neexistuje, vrátí prázdný seznam.
2. `pridej_kontakt(nazev, jmeno, telefon, email="")` přidá nový kontakt (slovník s klíči `jmeno`, `telefon`, `email`) a uloží soubor. Pokud už kontakt se stejným jménem existuje (na velikosti písmen nezáleží), nic nezmění a vrátí `False`, jinak `True`.
3. `najdi(nazev, text)` vrátí seznam kontaktů, jejichž jméno obsahuje `text` (na velikosti písmen nezáleží).
4. `smaz_kontakt(nazev, jmeno)` smaže kontakt s přesně tímto jménem (bez ohledu na velikost písmen) a vrátí `True`. Pokud takový není, vrátí `False`.
5. `vypis(nazev)` vrátí text s kontakty seřazenými podle jména, každý na řádku ve tvaru `Eva Nováková: 777111222`, řádky oddělené `\n`. Pro prázdný seznam vrátí `Žádné kontakty.`

Soubor ukládejte s odsazením 2 a čitelnou češtinou (`ensure_ascii=False`).
