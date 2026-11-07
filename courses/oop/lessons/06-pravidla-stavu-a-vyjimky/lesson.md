## Metoda odpovídá i za platný výsledek

Zásoba už má domluvené rozhraní. Teď zajistíme, aby běžné operace nevytvořily záporný nebo jinak nevhodný počet. Pravidlo, které má platit po každé úspěšné operaci, se někdy nazývá **invariant**. Zde je jednoduché: stav je nezáporné celé číslo.

Veřejné metody zůstávají stejné jako minule. Volající tak nepotřebuje měnit způsob příjmu nebo výdeje, jen musí počítat s odmítnutým požadavkem.

## Nejdříve ověřit, potom přiřadit

```python
if type(kolik) is not int or kolik <= 0:
    raise ValueError("Příjem musí být kladný celý počet")
self._pocet += kolik
return self._pocet
```

`type(kolik)` vrací skutečný typ hodnoty. Požadujeme přímo int, protože množství vyjadřuje celé kusy. Text `"3"`, desetinné číslo 3.0 nebo hodnoty True a False typu bool zde za počet nepovažujeme. `or` umožní odmítnout špatný typ ještě před číselným porovnáním.

Raise vytvoří a vyvolá výjimku ValueError. Tím se běžné provádění metody v tomto místě ukončí; k následujícímu přičtení se nedojde. Neplatnou hodnotu nepřevádíme automaticky ani nezamlčíme vrácením nuly.

Počáteční počet v konstruktoru může být 0. Příjem a výdej naopak požadují **kladné** množství, tedy alespoň 1. Výdej navíc nesmí překročit aktuální stav. Vydání přesně všech dostupných kusů je platné a vrátí nulu.

## Výjimka nevrací změny zpět

Kdyby metoda nejdřív odečetla 6 kusů z pěti a teprve potom vyvolala chybu, v objektu by zůstalo -1. Samotná výjimka dřívější přiřazení neodvolá. Proto všechny podmínky ověříme před změnou.

Při odmítnutí musí zůstat původní počet i název. Také není správné neplatný výdej potichu omezit na počet zbývajících kusů. Volající žádal konkrétní operaci a má se dozvědět, že nebyla provedena.

## Co udělá volající

```python
try:
    knihy.vydej(6)
except ValueError:
    print("Nedostupný výdej odmítnut.")
```

Try zkusí operaci, except zachytí domluvený druh chyby. Výpis patří volajícímu, ne skladové metodě. Po tomto bloku může program dál číst stav a nabídnout jiný požadavek. Nezachytáváme obecně každou výjimku programu.

Ukázka odmítne šest kusů z pěti a vypíše stále 5. Potom vydá přesně pět na nulu a přijme dva nové kusy. Zkuste neplatný příjem -1, nulový výdej nebo text místo čísla; po odmítnutí ověřte původní stav.

## Váš úkol

Doplňte ochranu třídy Zasoba. Konstruktor přijme jen nezáporný int. Prijmi přijme jen kladný int, vydej navíc ověří dostatek kusů. Každou neplatnou hodnotu odmítněte výjimkou ValueError před změnou stavu. Bool, čísla s desetinnou tečkou i texty se odmítají.

Úspěšné operace zachovávají rozhraní minulé lekce: stav vrací současný počet a nic nemění, příjem i výdej vracejí nový počet. Název je zadaný řetězec. Neplatná konstrukce nevytváří použitelnou zásobu a odmítnutá metoda nepoškodí existující objekt.
