## Více řádků z generátoru

Vytvořte **pridej_vice(con, pomucky)** pro iterovatelnou posloupnost dvojic (nazev, kusy), může to být jednorázový generátor. Vložte všechny řádky pomocí oddělených SQL parametrů a vraťte None. Prázdná dávka je platná.

`executemany` opakuje stejný příkaz pro více sad parametrů; neposkytuje seznam lastrowid všech řádků. Vstupní hodnoty neměňte, chybu integritních pravidel neskrývejte a sami neukončujte spojení ani transakci. Pozor: executemany samo nezaručuje, že chyba vrátí celou dávku. Při autocommit=True mohou už dřívější řádky zůstat uložené. Celek ochrání transakce v lekci 5.
