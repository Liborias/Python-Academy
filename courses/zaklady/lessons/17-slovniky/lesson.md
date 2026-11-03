## Hodnoty podle jména

Seznam najde prvek podle **pozice** (`seznam[0]`). Často se ale hodí najít hodnotu podle **názvu**, například telefon podle jména. K tomu slouží **slovník** (`dict`). Skládá se z dvojic **klíč: hodnota** ve složených závorkách:

```python
kontakt = {"jmeno": "Eva", "vek": 31}
print(kontakt["jmeno"])   # Eva
```

Do hranatých závorek se píše **klíč**. Klíčem bývá nejčastěji text nebo číslo. Hodnotou může být cokoli, třeba číslo, text nebo seznam.

## Přidání a přepsání

Stejný zápis slouží k přidání i ke změně. Pokud klíč ve slovníku ještě není, vznikne. Pokud už existuje, jeho hodnota se přepíše:

```python
kontakt["email"] = "eva@example.com"   # nový klíč
kontakt["vek"] = 32                    # přepsání stávající hodnoty
```

Počet dvojic zjistíte funkcí `len(kontakt)`.

## Chybějící klíč

Když se zeptáte na klíč, který ve slovníku není, Python skončí chybou `KeyError`. Další lekce ukáže, jak se jí bezpečně vyhnout.

> Klíče ve slovníku jsou jedinečné. Dvě dvojice se stejným klíčem existovat nemohou, novější hodnota přepíše starší.

## Váš úkol

1. `vytvor_kontakt(jmeno, telefon)` vrátí slovník s klíči `"jmeno"` a `"telefon"`.
2. `zmen_telefon(kontakt, novy)` přepíše telefon ve slovníku a slovník vrátí.
3. `pridej_email(kontakt, email)` přidá klíč `"email"` a slovník vrátí.
