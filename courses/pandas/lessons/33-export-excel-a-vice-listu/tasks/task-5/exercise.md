### Přečíst a ověřit hotový list

Tabulka má kod/nazev str a cena float64 bez chybějících hodnot, včetně textových kódů 001 a NA. Existující sešit může mít jiné listy. Vraťte bool, zda zadaný list souhlasí obsahem, sloupci a pořadím bez původního indexu. Čísla s tolerancí 1e-12, text přesně. Chybné schéma či neexistující list vraťte jako False. Sešit ani tabulku neměňte.

Doplňte `over_excel(tabulka, cesta, list)`. Pod zadáním lze zobrazit možné řešení.
