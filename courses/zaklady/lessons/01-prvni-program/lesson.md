## Počítač dělá, co mu napíšete

Program v Pythonu je text, který počítač čte shora dolů, řádek po řádku. Nejjednodušší je funkce `print()` (hotový kus kódu s jménem, funkce si později vysvětlíme podrobně): **vypíše** to, co jí dáte do závorek.

```python
print("Ahoj")
```

Text se píše do uvozovek (jednoduchých `'` nebo dvojitých `"`). Takovému textu se říká **řetězec**. Čísla se píší bez uvozovek.

- `print("Ahoj")` vypíše text
- `print(42)` vypíše číslo
- `print("a", "b")` vypíše obě hodnoty oddělené mezerou
- `print("ha" * 3)` vypíše `hahaha`: text lze **násobit** celým číslem

## Komentáře

Vše za znakem `#` Python ignoruje. Komentáře jsou poznámky pro lidi, vysvětlují, **proč** kód něco dělá.

> Zapomenutá uvozovka nebo závorka je nejčastější začátečnická chyba. Python pak napíše `SyntaxError` a ukáže řádek, kde se zarazil.

## Váš úkol

Napište program, který vypíše dva řádky: `Ahoj, světe!` a pod ním `Začínám s Pythonem.`
