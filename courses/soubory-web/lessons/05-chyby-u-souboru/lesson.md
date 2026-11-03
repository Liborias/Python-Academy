## Soubor tam být nemusí

Při práci se soubory vzniká víc chyb než u čistých výpočtů: soubor nemusí existovat, název může být špatně napsaný, nebo místo souboru ukazuje cesta na složku. Chybu `FileNotFoundError` zatím neznáte, vznikne při pokusu otevřít soubor, který neexistuje:

```python
open("neexistuje.txt", encoding="utf-8")   # FileNotFoundError
```

Chyby ze souborů se zachytávají `try` a `except`, tak jako v lekcích o výjimkách:

```python
try:
    with open("data.txt", encoding="utf-8") as soubor:
        text = soubor.read()
except FileNotFoundError:
    text = ""
```

## Nejčastější chyby u souborů

| Výjimka | Kdy vznikne |
|---|---|
| `FileNotFoundError` | soubor neexistuje |
| `IsADirectoryError` | cesta ukazuje na složku, ne na soubor |
| `PermissionError` | na soubor nemáte oprávnění |
| `UnicodeDecodeError` | soubor není v kódování UTF-8 |
| `ValueError` | řádek nejde převést na číslo |

První tři jsou **podtypy** obecnější chyby `OSError` (výjimky mají hierarchii: `FileNotFoundError` je zvláštní druh `OSError`, a proto ji `except OSError:` také zachytí). Pokud je chcete zachytit společně, napište `except OSError:`. To je i bezpečnější volba mezi počítači: když otevřete složku, Windows hlásí `PermissionError`, zatímco Linux a macOS `IsADirectoryError`.

## Kontrola předem, nebo zachycení chyby

Soubor lze předem ověřit pomocí `Path("data.txt").exists()`. Lepší bývá chybu rovnou zachytit: mezi kontrolou a čtením se může soubor ztratit.

## Chyby uvnitř dat

Špatně napsaný soubor způsobí `ValueError`. Pokud jeden špatný řádek nemá zastavit zpracování celého souboru, dá se výjimka zachytit **uvnitř cyklu**, špatné řádky se přeskočí.

## Váš úkol

1. `nacti_bezpecne(nazev, vychozi="")` vrátí obsah souboru. Pokud soubor neexistuje, nebo cesta není soubor, vrátí `vychozi`.
2. `nacti_cisla_bezpecne(nazev)` vrátí seznam celých čísel ze souboru (jedno na řádek). Špatné řádky (text) i prázdné řádky přeskočí. Pokud soubor neexistuje, vrátí prázdný seznam.
3. `zaloha(nazev)` zkopíruje soubor `nazev` do souboru `nazev + ".bak"` a vrátí `True`. Pokud soubor neexistuje, nic nevytváří a vrátí `False`.
