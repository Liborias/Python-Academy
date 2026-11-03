## Společná pravidla zápisu

Python má oficiální doporučení pro psaní kódu, **PEP 8**. Díky němu vypadají programy různých autorů podobně a snadno se čtou. Nejdůležitější body:

- **Jména:** proměnné a funkce malými písmeny s podtržítky (`pocet_zaku`), ne `pocetZaku`. Konstanty velkými písmeny.
- **Odsazení:** čtyři mezery, žádné tabulátory.
- **Délka řádku:** nejvýš 79 znaků (mnoho projektů používá 88).
- **Prázdné řádky:** dva mezi funkcemi na úrovni souboru.
- **Mezery:** kolem operátorů a za čárkou: `a + b`, `f(x, y)`, ale ne `f( x , y )`.

## Docstring

Každá funkce by měla mít popis ve třech uvozovkách hned pod řádkem s `def`. Napište, **co** funkce dělá, nikoli jak. Stačí jedna věta.

```python
def pocet_sudych(seznam):
    """Vrátí počet sudých čísel v seznamu."""
```

## Ruff ve VSCodium

Ruff je rychlý nástroj, který styl hlídá a umí ho i opravovat. Ve VSCodium je jako rozšíření `charliermarsh.ruff` (nastavení najdete ve složce `.vscode` vašeho pracovního prostoru):

- chyby podtrhává v kódu a vypisuje v panelu **Problémy** (výchozí sada pravidel hlídá hlavně skutečné chyby, například nepoužité importy a proměnné, a ne všechna pravidla PEP 8, třeba jména nebo prázdné řádky; další se zapínají v nastavení Ruffu),
- celý soubor naformátuje příkazem **Formátovat dokument** (Windows Shift+Alt+F, Linux Ctrl+Shift+I, macOS Shift+Option+F). Výchozí délka řádku je 88 znaků, kontrola v této lekci je přísnější a chce nejvýš 79.

Pokud rozšíření ve VSCodium nenajdete nebo nefunguje, nainstalujte `ruff` do prostředí příkazem `pip install ruff` a spusťte v terminálu `ruff check .` a `ruff format .`.

> Nástroje formátují vzhled, ale nepoznají, jestli je kód správně. To si ověřujete testy.

## Váš úkol

Napište tři funkce, které dodržují pravidla stylu:

1. `secti_seznam(seznam)` vrátí součet čísel.
2. `nejvetsi_rozdil(seznam)` vrátí rozdíl největšího a nejmenšího čísla.
3. `pocet_sudych(seznam)` vrátí počet sudých čísel v seznamu.

Požadavky: **každá funkce má docstring**, všechna jména jsou malými písmeny s podtržítky, řádky nejsou delší než 79 znaků, mezi funkcemi jsou **dva prázdné řádky** a odsazení tvoří mezery, ne tabulátory.
