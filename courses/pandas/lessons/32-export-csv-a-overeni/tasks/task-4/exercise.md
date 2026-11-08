### UTF-8 s BOM pro některé importy

Tabulka má kod/nazev str a hodnota float64 bez chybějících hodnot, libovolný řádkový index. Text může obsahovat středník, uvozovky, nový řádek, diakritiku i doslovné NA. Uložte CSV s UTF-8 BOM pomocí utf-8-sig. Ostatní pravidla zůstávají: středník, desetinná čárka, hlavička bez indexu. Vraťte Path; prázdná tabulka je platná, zdroj neměňte. BOM pomáhá některým importům Excelu rozpoznat kódování, nenahrazuje výběr oddělovače a textového typu kódu.

Doplňte `uloz_pro_excel(tabulka, cesta)`. Pod zadáním lze zobrazit možné řešení.
