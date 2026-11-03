## Hra podle nápovědy

První mini-projekt spojí slovníky, funkce, náhodu a vstup od uživatele. Počítač si vylosuje planetu, ukáže nápovědu (vzdálenost od Slunce a průměr) a hráč hádá, dokud neuhodne.

Data jsou ve slovníku slovníků, který najdete v editoru:

```python
PLANETY = {
    "Merkur": {"vzdalenost": 58, "prumer": 4879},
    "Mars": {"vzdalenost": 228, "prumer": 6779},
}
print(PLANETY["Mars"]["prumer"])   # 6779
```

Vzdálenost je v milionech kilometrů a průměr v kilometrech.

## Kostra programu

Dobrý program se skládá z malých funkcí, každá dělá jednu věc. Spuštění hry se píše na konec souboru do bloku:

```python
if __name__ == "__main__":
    hra(PLANETY, vyber_planetu(PLANETY))
```

Podmínka je splněna jen tehdy, když soubor **spustíte přímo**. Když ho jiný program nebo kontrola jen načte (importuje), hra se sama nezapne. Tak se dají funkce zkoušet samostatně.

## Váš úkol

Napište pět částí:

1. `napoveda(planety, jmeno)` vrátí text `Je 228 mil. km od Slunce a má průměr 6779 km.` (čísla podle planety). **Jméno planety v textu být nesmí.**
2. `je_spravne(tip, jmeno)` vrátí `True`, pokud se tip shoduje se jménem. Mezery na okrajích a velikost písmen nehrají roli.
3. `vyber_planetu(planety)` vrátí náhodné jméno planety ze slovníku.
4. `pocet_pokusu(tipy, jmeno)` dostane seznam tipů a vrátí pořadí (od 1) prvního správného tipu, nebo `None`, pokud tam žádný není.
5. `hra(planety, jmeno)` vypíše nápovědu a v cyklu se ptá `input("Která planeta to je? ")`, dokud hráč neuhodne. Po správném tipu vypíše `Správně!` a **vrátí** počet pokusů. Při špatném tipu vypíše `Ne, zkuste to znovu.`

Na konci souboru nechte blok `if __name__ == "__main__":`, který hru spustí.
