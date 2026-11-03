## Od dat k odpovědím

Teď spojíte vše z minulých lekcí: načíst tabulku a z řádků **vyčíst odpovědi**. Soubor `prodej.csv` obsahuje prodej ovoce:

```text
mesic,zbozi,kusy,cena
leden,jablka,120,25
...
```

Typické otázky: kolik jsme utržili za které zboží, který měsíc byl nejlepší, které řádky mají nejvíc kusů.

## Řazení podle zvoleného pole

Funkce `sorted` umí řadit i slovníky, ale musí vědět, **podle čeho**. Parametr `key` dostane funkci, která z řádku vybere hodnotu k porovnání. Nejjednodušší je zapsat ji krátce pomocí `lambda`:

```python
radky = [{"zbozi": "a", "kusy": 5}, {"zbozi": "b", "kusy": 9}]
sorted(radky, key=lambda r: r["kusy"])                  # od nejmenšího
sorted(radky, key=lambda r: r["kusy"], reverse=True)    # od největšího
```

Zápis `lambda r: r["kusy"]` znamená „funkce, která pro řádek `r` vrátí `r["kusy"]`“. Parametr `reverse=True` otočí pořadí. Řádky se stejnou hodnotou zůstanou ve **stejném pořadí**, v jakém byly původně.

Výběr části seznamu (řez): `seznam[:3]` vybere první tři prvky.

## Součty podle skupiny

Postup známe z počítání ve slovníku: klíč je skupina (zboží, měsíc), hodnota průběžný součet.

```python
trzby = {}
for r in radky:
    trzby[r["zbozi"]] = trzby.get(r["zbozi"], 0) + r["kusy"] * r["cena"]
```

Pro slovník najde klíč s největší hodnotou `max(trzby, key=trzby.get)`.

## Váš úkol

Řádky tabulky jsou slovníky s texty `mesic`, `zbozi` a čísly `kusy`, `cena`.

1. `nacti_prodej(nazev)` načte CSV a vrátí seznam slovníků, kde `kusy` a `cena` jsou **celá čísla**.
2. `trzby_podle_zbozi(radky)` vrátí slovník `{zboží: tržba}`, kde tržba řádku je `kusy * cena`.
3. `nejlepsi_mesic(radky)` vrátí měsíc s největší celkovou tržbou.
4. `nejvic_kusu(radky, n)` vrátí `n` řádků s nejvíce kusy, od největšího. Při shodě zůstane původní pořadí.
