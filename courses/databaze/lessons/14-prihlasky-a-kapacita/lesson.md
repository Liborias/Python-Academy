## Každá přihláška patří ke kroužku

Přihlášky mají vlastní id a krouzek_id. Vazba chrání existenci kroužku, UNIQUE(krouzek_id, clen) zakazuje stejné jméno ve stejném kroužku. Stejné jméno v jiném kroužku je dovolené. Jde o cvičný model podle přesného jména; dvě stejnojmenné osoby by potřebovaly samostatnou tabulku členů s id.

```python
# Kapacita 2 dovoluje přijetí při počtu 1, nikoli při počtu 2.
kapacita = 2
for pocet in [0, 1, 2]:
    print(pocet, 'lze přijmout:', pocet < kapacita)
```

Přihlášení v jedné transakci zjistí kapacitu, spočítá přihlášky a teprve pak vloží nový řádek. Číslo v popisku okna je jen zobrazení; o přijetí rozhodne model nad aktuálními daty. Nejprve ověřujeme plnost, proto už plný kroužek hlásí „Kroužek je plný.“ i při opakovaném jménu.

## Získání souvisejících dat

Souhrn propojí krouzky LEFT JOIN prihlasky. COUNT(p.id) vrátí pro prázdný kroužek nulu; COUNT(*) by spočítal i pomocný řádek levého spojení. Výpis přihlášek má vlastní mapu self.clenove: odhlášení použije id přihlášky, ne id kroužku či index seznamu.

Odhlášení záznam odstraní a uvolní místo. Opakovaný požadavek vrátí False bez další změny. Po odhlášení se zruší výběr přihlášky; další kliknutí bez výběru nic nemaže. Přihlášky zatím netvoří trvalou historii jako výpůjčky předchozího projektu.

## Váš úkol

Rozšiřte Model a Aplikace z přiložených upravy.py. Model: `prihlasky(ident)` vrátí [(id_přihlášky, člen)] pro kroužek v pořadí id, chybějící/prázdný kroužek dává []. `prihlas(ident, clen)` ořízne jméno, odmítne prázdné, v transakci najde kapacitu a počet; chybějící kroužek je ValueError „Kroužek už neexistuje.“, plný „Kroužek je plný.“ Jinak INSERT s parametry a skutečné id. Duplicitní jméno, pokud ještě zbývá místo, je IntegrityError.

`odhlas(ident)` maže podle id přihlášky a vrací bool podle rowcount. `souhrn()` vrátí [(id_kroužku, název, kapacita, počet_přihlášek)] v pořadí id, i pro prázdné kroužky.

GUI obnov_prihlasky načte data pro vybraný kroužek, jinak prázdný seznam. V Listboxu zobrazí `id: člen`, vedle „Obsazeno počet / kapacita“, bez výběru „Vyberte kroužek pro přihlášky.“ Pridej a uprav z předchozího formuláře dál fungují; připravené vyber/novy/obnov zajistí obnovení souvisejícího panelu.

GUI prihlas bez výběru oznámí „Nejprve vyberte kroužek.“ Chyby zobrazí, jméno zachová; duplicitu vysvětlí „Člen už je v tomto kroužku přihlášený.“ Po úspěchu obnoví přihlášky, vyčistí jméno a oznámí „Člen přihlášen.“ GUI odhlas vyžaduje výběr přihlášky („Nejprve vyberte přihlášku.“), použije její skutečné id, obnoví a oznámí „Člen odhlášen.“ nebo „Přihláška už neexistuje.“

Projekt je pro jednoho místního správce. Nepřidává automatické opakování při SQLITE_BUSY ani síťové přístupy. Model a widgety používejte ve stejném hlavním vlákně.
