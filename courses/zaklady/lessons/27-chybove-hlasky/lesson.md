## Chyba není selhání

Každý programátor vidí chyby denně. Python vám u nich říká, **co** se stalo i **kde**. Stačí hlášku umět číst. Příklad:

```text
Traceback (most recent call last):
  File "reseni.py", line 8, in <module>
    print(posledni([1, 2, 3]))
  File "reseni.py", line 4, in posledni
    return seznam[len(seznam)]
IndexError: list index out of range
```

Čtěte ji **odspodu**:

1. Poslední řádek je **druh chyby** a vysvětlení: `IndexError: list index out of range` (index mimo seznam).
2. Řádky nad ním ukazují cestu, kudy program došel k chybě. Nejblíž k chybě je ten **poslední** zápis `line 4`. Podívejte se právě na tento řádek.

## Nejčastější chyby začátečníků

| Chyba | Obvyklá příčina |
|---|---|
| `SyntaxError` | chybí dvojtečka, uvozovka nebo závorka. Python ukáže řádek, na kterém to zjistil, příčina bývá i na řádku před ním |
| `IndentationError` | špatné odsazení |
| `NameError` | proměnná neexistuje: překlep nebo ji ještě nikdo nevytvořil |
| `TypeError` | operace s nevhodným typem, například `"5" + 1` |
| `IndexError` | index mimo seznam: poslední prvek má index `len(seznam) - 1` |
| `KeyError` | klíč ve slovníku není |

> Chyby opravujte **po jedné** od první, kterou Python ohlásí. Po opravě program spusťte znovu. Další chyby se často vyřeší samy.

## Váš úkol

Kód v editoru obsahuje čtyři chyby. Spusťte ho tlačítkem Spustit, přečtěte hlášku a opravujte jednu po druhé, dokud všechny čtyři funkce nefungují podle popisu v komentáři.
