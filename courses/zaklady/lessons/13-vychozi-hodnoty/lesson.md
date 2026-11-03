## Parametr, který není povinný

Parametru můžete dát **výchozí hodnotu**. Když ji volající nezadá, použije se ta výchozí:

```python
def zdrav(jmeno, pozdrav="Ahoj"):
    return f"{pozdrav}, {jmeno}!"

zdrav("Eva")             # Ahoj, Eva!
zdrav("Eva", "Čau")      # Čau, Eva!
```

Parametry s výchozí hodnotou musí být **za** povinnými.

## Pojmenované argumenty

Při volání můžete argumenty pojmenovat. Pak nezáleží na pořadí a kód je čitelnější:

```python
zdrav(pozdrav="Dobrý den", jmeno="Jan")
```

Hotové funkce to používají také: `print("a", "b", sep="-")` nebo `print("Konec", end="!")`.

> Nikdy nepoužívejte jako výchozí hodnotu prázdný seznam (`def f(x, seznam=[])`). Takový seznam se sdílí mezi všemi voláními a překvapí vás. Správně je výchozí hodnota `None` a seznam se vytvoří uvnitř funkce.

## Váš úkol

Napište funkci `zdrav(jmeno, pozdrav="Ahoj")`, která vrátí text `Ahoj, Eva!` (s příslušným pozdravem). Dále funkci `mocnina(zaklad, exponent=2)`, která vrátí `zaklad` umocněný na `exponent` (operátor `**`).
